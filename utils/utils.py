from androguard.core.bytecodes.apk import APK
import os, platform, zipfile, config


def get_apk_information(_file):
    '''
    get apk information by androguard
    params:
    _file: apk file path

    return:
    1. apkname: apk name
    2. apkcode: apk version code, eg: 222, 333
    3. apkiconpath: get icon path
    '''
    apkinformation = APK(_file)

    apkname = apkinformation.get_app_name()
    apkcode = apkinformation.get_androidversion_code()
    apkiconpath = apkinformation.get_app_icon()
    # packagename = apkinformation.get_package()

    return apkname, apkcode, apkiconpath


def parseAPKICO(apk, icon_name):
    # print(platform.system())
    # systemName = platform.system()
    # if systemName != 'Windows' or systemName != 'Linux':
    #     raise TypeError('unknown system type, only support Linux and Windows OS')
    #
    # if systemName == 'Windows':
    #     aaptTool = os.path.join(config.PARSE_APKICON_TOOLS_PATH, 'Windows/aapt_64.exe')
    #     cmd = "{} dump badging {} | findstr application-icon-120".format(aaptTool,  )

    apkname, apkcode, apkiconpath = get_apk_information(apk)
    if '{}.png'.format(apkname) not in config.SAVE_APKICON_PATH:
        zip = zipfile.ZipFile(apk)
        iconData = zip.read(apkiconpath)
        saveIconName = os.path.join(config.SAVE_APKICON_PATH, '{}.png'.format(icon_name))
        with open(saveIconName, 'w+b') as saveIconFile:
            saveIconFile.write(iconData)
        return apkname, apkcode
    else:
        return apkname, apkcode
