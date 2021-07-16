import logging
import os

import android_tools.utils

rm_files = ("a", "so", "jar", "jpg", "png", "PNF", "zip", "gz", "ogg",
            "db", "lic", "apk", "ttf", "pdf", "mp3", "mp4", "tflite",
            "pk8", "pem", "txt", "jks", "exe", "dat",
            "jet" "bat", "wav", "gif", "bat", "properties", "preset",
            "dhex", "ko", "bin", "bmp", "xws", "ccu",
            "ddr", "hex", "img", "dll", "yuv", "darwin", "der")
rm_folders = (".git",)
rm_relative_paths = ("frameworks/neuropilot", "frameworks/opt/agps_lib",
                     "frameworks/opt/mdlogger_lib", "frameworks/opt/libimsma",
                     "frameworks/opt/mdm_lib", "frameworks/opt/mdml_lib",
                     "frameworks/opt/memoryDumpEncoder_lib",
                     "frameworks/opt/duraspeed_lib", "frameworks/opt/jpe_lib",
                     "frameworks/opt/libimsma_bin_lib", "frameworks/base/agps",
                     "external/aee", "external/doeapp_lib")
dest = "/home/xupeng/work/code/freemeos-code/EAL4/FreemeOwnRate-tmp/system/instrument"

if __name__ == '__main__':
    logging.basicConfig(
        # filename="create_patch.log",
        # filemode='a',
        level=logging.DEBUG,
        # format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
        format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'
    )

    sorted_result = sorted(android_tools.utils.do_statistics(
        dest, rm_files, rm_folders, rm_relative_paths).items(),
                           key=lambda item: (item[1][1]),
                           reverse=True)

    total_size = 0
    statistics_file = os.path.normpath(os.path.join(os.path.abspath(dest), "statistics.txt"))
    statistics_fd = open(statistics_file, "w")
    for sorted_item in sorted_result:
        key = sorted_item[0]
        # value_list is [file_count, file_total_size, [file_lists]]
        value_list = sorted_item[1]
        file_size = value_list[1] / 1024
        logging.debug("{} file appears {} times, total size {:.2f}kb"
                      .format(key, value_list[0], file_size))
        summary = "{} file appears {} times, total size {:.2f}kb:" \
            .format(key, value_list[0], file_size)
        total_size += file_size
        statistics_fd.writelines(summary)
        statistics_fd.writelines("\n")
        for appear in value_list[2]:
            statistics_fd.write("\t")
            statistics_fd.write(appear)
            statistics_fd.write("\n")
    statistics_fd.close()
    logging.debug("total_size: {:.4}MB".format(total_size / 1024))
