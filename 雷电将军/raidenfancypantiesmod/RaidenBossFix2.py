# Author: NK#1321 raiden boss fix, if you used it to fix your raiden pls give credit for "Nhok0169"
# Special Thanks:
#   nguen#2011 (for support)
#   SilentNightSound#7430 (for internal knowdege so wrote the blendCorrection code)
#   HazrateGolabi#1364 (for being awesome, and improving the code)


import os
import configparser
import re
import struct



vg_remap = {'0':'0','1':'1','2':'2','3':'3','4':'4','5':'5','6':'6','7':'7','8':'60','9':'61','10':'66','11':'67',
             '12':'8','13':'9','14':'10','15':'11','16':'12','17':'13','18':'14','19':'15','20':'16','21':'17',
             '22':'18','23':'19','24':'20','25':'21','26':'22','27':'23','28':'24','29':'25','30':'26','31':'27',
             '32':'28','33':'29','34':'30','35':'31','36':'32','37':'33','38':'34','39':'35','40':'36','41':'37',
             '42':'38','43':'39','44':'40','45':'41','46':'42','47':'94','48':'43','49':'44','50':'45','51':'46',
             '52':'47','53':'48','54':'49','55':'50','56':'51','57':'52','58':'53','59':'54','60':'55','61':'56',
             '62':'57','63':'58','64':'59','65':'114','66':'116','67':'115','68':'117','69':'74','70':'62','71':'64',
             '72':'106','73':'108','74':'110','75':'75','76':'77','77':'79','78':'87','79':'89','80':'91','81':'95',
             '82':'97','83':'99','84':'81','85':'83','86':'85','87':'68','88':'70','89':'72','90':'104','91':'112',
             '92':'93','93':'63','94':'65','95':'107','96':'109','97':'111','98':'76','99':'78','100':'80','101':'88',
             '102':'90','103':'92','104':'96','105':'98','106':'100','107':'82','108':'84','109':'86','110':'69',
             '111':'71','112':'73','113':'105','114':'113','115':'101','116':'102','117':'103'}
maxVGindex = 117

# Diabling the OLD ini
def dis_ini(file):
    print("Cleaning up and disabling the OLD STINKY ini")
    os.rename(file, os.path.join(os.path.dirname(file), "DISABLED") + os.path.basename(file))

# Collect the ini
def collect_ini(path):
    print("Finding the ini")
    ini_file = ''
    ini_file = [x for x in os.listdir(".") if ".ini" in x]
    if len(ini_file) != 1:
        print("ERROR: Unable to find *.ini file. Ensure it is in the folder, and only one *.ini file exists")
        return
    ini_file = ini_file[0]
    return ini_file
# correcting the blend file
def blendCorrection():
    print("correcting the blend file")
    blend_file = [x for x in os.listdir(".") if "Blend.buf" in x]
    if len(blend_file) != 1:
        print("ERROR: Unable to find CharNameBlend.buf. Ensure it is in the folder, and only one Blend.buf exists")
        return
    blend_file = blend_file[0]

    with open(blend_file, "rb") as f:
        blend_data = f.read()

    if len(blend_data)%32 != 0:
        print("ERROR: Blend file format not recognized")
        return

    result = bytearray()
    for i in range(0,len(blend_data),32):
        blendweights = [struct.unpack("<f", blend_data[i+4*j:i+4*(j+1)])[0] for j in range(4)]
        blendindices = [struct.unpack("<I", blend_data[i+16+4*j:i+16+4*(j+1)])[0] for j in range(4)]
        outputweights = bytearray()
        outputindices = bytearray()
        for weight, index in zip(blendweights, blendindices):
            if weight != 0 and index <= maxVGindex:
                index = int(vg_remap[str(index)])
            outputweights += struct.pack("<f", weight)
            outputindices += struct.pack("<I", index)
        result += outputweights
        result += outputindices
    FixedBlendName = f"{blend_file.split('Blend.buf')[0]}RemapBlend.buf"
    with open(FixedBlendName, "wb") as f:
        f.write(result)
    print('Blend file correction done')
    return FixedBlendName


#add the needed lines on the ini file and copy the draw number
pattern = re.compile(r"TextureOverride(\w+)Blend")
parser = configparser.ConfigParser()

ini_file = collect_ini('.')
parser.read(ini_file)
for k in dict(parser).keys():
    if pattern.match(k) != None:
        blend = dict(parser[k])
if blend["draw"]:
    draw: str = blend["draw"]

fixedBlendName = blendCorrection().split('.')[0]

addFix = f'\n;raiden boss fixed by NK#1321 if you used it for fix your raiden pls give credit for "Nhok0169"\n;thank nguen#2011 SilentNightSound#7430 and HazrateGolabi#1364 for support\n\n[TextureOverride{fixedBlendName}]\nhash = fe5c0180\nvb1 = Resource{fixedBlendName}\nhandling = skip\ndraw = {draw} \n\n[Resource{fixedBlendName}]\ntype = Buffer\nstride = 32\nfilename = {fixedBlendName}.buf\n\n\n'

original = ''
with open(ini_file, "r") as f:
    original = f.read()
dis_ini(ini_file)

# writing the fixed file
print("making the fixed ini file")
with open(ini_file, "w") as f:
    f.write(addFix)
    f.write(original)


print("ENJOY")