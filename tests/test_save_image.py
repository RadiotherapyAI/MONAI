# Copyright 2020 - 2021 MONAI Consortium
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import tempfile
import unittest

import torch
from parameterized import parameterized

from monai.transforms import SaveImage
from monai.utils.module import optional_import
from tests.utils import TEST_NDARRAYS

_, has_pil = optional_import("PIL")
_, has_nib = optional_import("nibabel")

exts = [ext for has_lib, ext in zip((has_nib, has_pil), (".nii.gz", ".png")) if has_lib]

TESTS = []
for p in TEST_NDARRAYS:
    for ext in exts:
        TESTS.append(
            [
                p(torch.randint(0, 255, (1, 2, 3, 4))),
                {"filename_or_obj": "testfile0" + ext},
                ext,
                False,
            ]
        )
        TESTS.append(
            [
                p(torch.randint(0, 255, (1, 2, 3, 4))),
                None,
                ext,
                False,
            ]
        )


class TestSaveImage(unittest.TestCase):
    @parameterized.expand(TESTS, skip_on_empty=True)
    def test_saved_content(self, test_data, meta_data, output_ext, resample):
        with tempfile.TemporaryDirectory() as tempdir:
            trans = SaveImage(
                output_dir=tempdir,
                output_ext=output_ext,
                resample=resample,
                # test saving into the same folder
                separate_folder=False,
            )
            trans(test_data, meta_data)

            filepath = "testfile0" if meta_data is not None else "0"
            self.assertTrue(os.path.exists(os.path.join(tempdir, filepath + "_trans" + output_ext)))


if __name__ == "__main__":
    unittest.main()
