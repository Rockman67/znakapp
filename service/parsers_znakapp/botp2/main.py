import sys
sys.path.append("/home/djangoapp/znakapp/service/parsers_znakapp/")
from botp2.kn_kz_parser import parsing_kn_kz
from botp2.krisha_kz_parser import parsing_krisha_kz
from botp2.kz_m2bomber_com_parser import parsing_kz_m2bomber
from botp2.nedvizhimostpro_kz_parser import parsing_nevdizhimostpro_kz
from botp2.olx_kz_parser import parsing_olx_kz

def main(value: str):
    try:
        if "www.kn.kz" in value:
            parsing_kn_kz(value)  # Not clear, only parsing and input
        elif 'krisha.kz' in value:
            parsing_krisha_kz(value)  # Clear
        elif "kz.m2" in value:
            parsing_kz_m2bomber(value)  # Not clear, only pars
        elif "nedvizhimostpro.kz" in value:
            parsing_nevdizhimostpro_kz(value)  # Not clear, only pars
        elif "olx.kz" in value:
            parsing_olx_kz(value)  # Not clear, only pars
    except Exception as ex:
        print(f'Parsing error: {ex}')

if __name__ == "__main__":
    value = sys.argv[1]
    main(value)


