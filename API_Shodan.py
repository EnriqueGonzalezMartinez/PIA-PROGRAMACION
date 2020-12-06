import shodan
import logging

def API(api_key,port):
        ips= []
        try:
            shodan_object= shodan.Shodan(api_key)
            results= shodan_object.search(f"port: {port} Anonymous user logged in")
            print("Hosts found possibly vulnerable = ", len(results["matches"]))

            if (results['matches'] != []):
                for match in results["matches"]:
                        ips.append(match["ip_str"])

                with open("Host_vulnerables.txt", "w") as file:
                    for ip in ips:
                        file.write(f'{ip}\n')

                print("Successfully generated file.")
            else:
                print('No possibly vulnerable hosts found.')
        except Exception as e:
            print('Wrong API KEY or range not available.')
            logg(e)


def logg(e):
    #cambiar el logger dependiendo del programa y se establece nivel 
    logger = logging.getLogger('Shodan')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('debug.log')
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    #se le asigna un formato
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.error(e)
