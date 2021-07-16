import logging
import os
import re

dest_path = "/home/xupeng/work/code/freemeos-code/EAL4/FreemeOwnRate-test"
filter_pattern = [
    re.compile(r'Copyright .*The Android Open Source Project', re.I),
    re.compile(
        r'Licensed under the Apache License, Version 2.0 \(the "License"\);'),
    re.compile(
        r'you may not use this file except in compliance with the License.'),
    re.compile(r'You may obtain a copy of the License at'),
    re.compile(r'http://www.apache.org/licenses/LICENSE-2.0'),
    re.compile(
        r'Unless required by applicable law or agreed to in writing, software'),
    re.compile(
        r'distributed under the License is distributed on an "AS IS" BASIS,'),
    re.compile(
        r'WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.'),
    re.compile(
        r'See the License for the specific language governing permissions and'),
    re.compile(r'limitations under the License'),
    re.compile(r'Universal Electronics Inc'),
    re.compile(r'Copyright .*Inc', re.I),
    re.compile(r'Copyright .*Ltd', re.I),
    re.compile(r'Copyright .*iFLYTEK', re.I),
    re.compile(r'MediaTek'),
    re.compile(r'MEDIATEK'),
    re.compile(r'^\s*\*+.*Copyright Statement', re.I),
    re.compile(
        r'protected under relevant copyright laws. The information contained herein is'),
    re.compile(
        r'information contained herein, in whole or in part, shall be strictly'),
    re.compile(r'prohibited'),
    re.compile(
        r'BY OPENING THIS FILE, RECEIVER HEREBY UNEQUIVOCALLY ACKNOWLEDGES AND AGREES'),
    re.compile(
        r'WARRANTIES, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED'),
    re.compile(
        r'WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE OR'),
    re.compile(
        r'RESPECT TO THE SOFTWARE OF ANY THIRD PARTY WHICH MAY BE USED BY,'),
    re.compile(
        r'TO LOOK ONLY TO SUCH THIRD PARTY FOR ANY WARRANTY CLAIM RELATING THERETO.'),
    re.compile(
        r'RECEIVER EXPRESSLY ACKNOWLEDGES THAT IT IS RECEIVER\'S SOLE RESPONSIBILITY TO'),
    re.compile(
        r'RELEASES MADE TO RECEIVER\'S SPECIFICATION OR TO CONFORM TO A PARTICULAR'),
    re.compile(
        r'protected under relevant copyright laws. The information contained herein'),
    re.compile(
        r'EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF'),
    re.compile(
        r'MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE OR NONINFRINGEMENT.'),
    re.compile(
        r'SOFTWARE OF ANY THIRD PARTY WHICH MAY BE USED BY, INCORPORATED IN, OR'),
    re.compile(
        r'THIRD PARTY FOR ANY WARRANTY CLAIM RELATING THERETO. RECEIVER EXPRESSLY ACKNOWLEDGES'),
    re.compile(
        r'THAT IT IS RECEIVER\'S SOLE RESPONSIBILITY TO OBTAIN FROM ANY THIRD PARTY ALL PROPER LICENSES'),
    re.compile(
        r'OR REFUND ANY SOFTWARE LICENSE FEES OR SERVICE CHARGE PAID BY RECEIVER TO'),
    re.compile(
        r'Modification based on code covered by the .*mentioned copyright'),
    re.compile(r'and/or permission notice'),

    re.compile(
        r'This software is protected by Copyright and the information contained'),
    re.compile(
        r'herein is confidential. The software may not be copied and the information'),
    re.compile(
        r'contained herein may not be used or disclosed except with the written'),
    re.compile(
        r'BY OPENING THIS FILE, BUYER HEREBY UNEQUIVOCALLY ACKNOWLEDGES AND AGREES'),
    re.compile(
        r'SPECIFICATION OR TO CONFORM TO A PARTICULAR STANDARD OR OPEN FORUM.'),
    re.compile(
        r'OR REFUND ANY SOFTWARE LICENSE FEES OR SERVICE CHARGE PAID BY BUYER TO'),
    re.compile(
        r'THE TRANSACTION CONTEMPLATED HEREUNDER SHALL BE CONSTRUED IN ACCORDANCE'),
    re.compile(
        r'WITH THE LAWS OF THE STATE OF CALIFORNIA, USA, EXCLUDING ITS CONFLICT OF'),
    re.compile(
        r'LAWS PRINCIPLES.  ANY DISPUTES, CONTROVERSIES OR CLAIMS ARISING THEREOF AND'),
    re.compile(
        r'RELATED THERETO SHALL BE SETTLED BY ARBITRATION IN SAN FRANCISCO, CA, UNDER'),
    re.compile(r'THE RULES OF THE INTERNATIONAL CHAMBER OF COMMERCE'),
]
ignore_folders = (".git",)


def check_text(line: str):
    for pattern in filter_pattern:
        if pattern.search(line):
            return True
    return False


def rm_filter_text(file_path: str):
    # logging.debug("filter file {}".format(file_path))
    target_file = "{}.modify".format(file_path)
    if not os.path.exists(file_path):
        logging.error("{} not exist".format(file_path))
        return
    else:
        try:
            with open(file_path) as source, open(target_file, 'w') as target:
                for line in source:
                    if not check_text(line):
                        target.write(line)
        except UnicodeDecodeError:
            logging.error("Error: can not open {}".format(file_path))
        else:
            source.close()
            target.close()
    if os.path.exists(target_file):
        os.rename(target_file, file_path)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'
    )
    # rm_filter_text("/home/xupeng/work/code/freemeos-code/EAL4/test/"
    #                "suw_recycler_template_header.xml")
    for root, dirs, files in os.walk(dest_path):
        for ignore_folder in ignore_folders:
            if root.find(ignore_folder) == -1:
                for file in files:
                    abs_file_path = os.path.normpath(os.path.join(root, file))
                    rm_filter_text(abs_file_path)
