import re

class OutFormat:

    @staticmethod
    def output_svg(infile,outfile,cityset):
        '''svgファイルへの出力

        citysetに登録されたcityクラスのデータをもとに
        svgファイルへ出力する．


        '''
        flag,rowNum,retflag=1,0,0
        ccobj,code = '',''

        f = open(outfile,'w',encoding='utf-8')
        for l in open(infile,encoding='utf-8'):
            l = l.rstrip()
            if re.search('use xlink:href',l):
                retflag=1
                f.write(l+'\n')
                continue
            if retflag==1 and l.startswith('<path style='):
                break
            if flag==1 and l.startswith('<path style="fill-rule:evenodd'):
                flag=1
                ccobj = re.search(r'<path (style="fill-rule.+;)fill:rgb\(.+?\);(fill-opacity.+$)',l)
                city = cityset.get_city_from_pathnum(rowNum)
                cityname = city.cityname
                color = city.colorcode
                f.write('<path class="cwtv {} {}" {}fill:{};{}\n'.format(code,cityname,ccobj.group(1),color,ccobj.group(2)))
                rowNum+=1
            elif l.startswith('<g style'):
                f.write(l+'\n')
                flag=0
                continue
            else:
                if l.startswith('<path style="fill-rule:even'):
                    continue
                else:
                    f.write(l+'\n')

        f.write('</g>\n</svg>\n')
        f.close()
