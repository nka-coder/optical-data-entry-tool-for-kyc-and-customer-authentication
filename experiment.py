from id_reader_utilities import unit_extraction, dataset_size, count_inaccuracy 
from id_reader_utilities import filter_mrz, mrz_improver, check_mrz_all_info, parse_mrz
from os import listdir

# Ground truth for the experiment with the dataset of cameroonian passport
actual_mrz_cmr = {
  "mrz_type": "TD3",
  "type": "P",
  "country": "CMR",
  "number": "01312168",
  "check_number": "4",
  "date_of_birth": "830408",
  "check_date_of_birth": "1",
  "expiration_date": "140611",
  "check_expiration_date": "5",
  "nationality": "CMR",
  "sex": "M",
  "names": "ADAMOU",
  "surname": "NCHANGE KOUOTOU"
}
# Ground truth for the experiment with the dataset of brazilian passport
actual_mrz_bra = {
  "mrz_type": "TD3",
  "type": "P",
  "country": "BRA",
  "number": "AA000000",
  "check_number": "0",
  "date_of_birth": "810110",
  "check_date_of_birth": "9",
  "expiration_date": "250814",
  "check_expiration_date": "",
  "nationality": "BRA",
  "sex": "F",
  "names": "JOANA",
  "surname": "SILVA COSTA"
}

def unit_experiment(images_folder, mrz_format, sample_size):
    """
    This function implements Max likelihood for one image set size equal to 'sample_size'.
    
    Input parameters:
    - images_folder: path to the folder containing images of the passport that need identity
                        information extraction
    - mrz_format: Actual identity information information into the identity document. Its format is
                described below
    Example:
    valid_mrz  = {
                    "mrz_type": "TD3",
                    "type": "P",
                    "country": "CMR",
                    "number": "01312168",
                    "check_number": "4",
                    "date_of_birth": "830408",
                    "check_date_of_birth": "1",
                    "expiration_date": "140611",
                    "check_expiration_date": "5",
                    "nationality": "CMR",
                    "sex": "M",
                    "names": "ADAMOU",
                    "surname": "NCHANGE KOUOTOU"
                }
    - sample_size: Nimber of images used to implement Max likelihood treatment of the identity document

    Return: None
    """
    filename_list = listdir(images_folder)
    mrz_tp = 0
    data_size = 0
    parsed_data_size = 0
    parsed_mrz_tp = 0
    improved_parsed_mrz_tp = 0
    improved_parsed_data_size = 0
    improved_data_size = 0
    improved_mrz_tp = 0
    mrz_list = []
    counter = 0

    for image in filename_list:
        
        try:
            mrz_data = unit_extraction(images_folder,image, mrz_format)
            mrz_tp += count_inaccuracy(mrz_data, mrz_format)
            data_size += dataset_size(mrz_data, mrz_format)

            parsed_mrz_data = parse_mrz(mrz_data, mrz_format)
            parsed_mrz_tp += count_inaccuracy(parsed_mrz_data, mrz_format)
            parsed_data_size += dataset_size(parsed_mrz_data, mrz_format)

            if counter < sample_size:
                # print(counter, image)
                mrz_list.append(mrz_data)
                counter +=1
            
            else:
                mrz_list.append(mrz_data)
                counter +=1
                improved_mrz = mrz_improver(mrz_list, mrz_format)
                improved_parsed_mrz = parse_mrz(improved_mrz, mrz_format)

                if check_mrz_all_info(improved_parsed_mrz) :
                    checked_digits_mrz = improved_parsed_mrz      
                    
                    improved_mrz_tp += count_inaccuracy(improved_mrz, mrz_format)
                    improved_data_size += dataset_size(improved_mrz, mrz_format)
     
                    improved_parsed_mrz_tp += count_inaccuracy(improved_parsed_mrz, mrz_format)
                    improved_parsed_data_size += dataset_size(improved_parsed_mrz, mrz_format)
                    break
                else:
                    print("Experiment didn't converge. Adding a sample image...")

        except:
            pass

    PCR_mrz = (data_size - mrz_tp) / data_size
    PCR_parsed_mrz = (parsed_data_size - parsed_mrz_tp) / parsed_data_size
    PCR_improved_mrz = (improved_data_size - improved_mrz_tp) / improved_data_size
    PCR_improved_parsed_mrz = (improved_parsed_data_size - improved_parsed_mrz_tp) / improved_parsed_data_size

    # Display the results of the experiment
    print('Per-Character Recognition (PCR):')
    print(f"- Passporteye:                            {PCR_mrz:.2f}")
    print(f"- Passporteye + Parsing:                  {PCR_parsed_mrz:.2f}")
    print(f"- Passporteye + Max likelihood:           {PCR_improved_mrz:.2f}")
    print(f"- Passporteye + Max likelihood + Parsing: {PCR_improved_parsed_mrz:.2f}")
    print(f"- Dataset size: {dataset_size(mrz_format, mrz_format)}")
    # print('Actual identity information:')
    # print(f"{mrz_format} \n")
    # print('Extracted identity information:')
    # print(f"{checked_digits_mrz} \n")
    return 


# Run the experiment and display the results
if __name__ == "__main__":
    """
    Execute this script to run the experiment and compare Passporteye and Passporteye + Max likelihood
    performance. It implements Max likelihood for image set size equal to 3,4,5,6 and 7.
    
    Input parameters:
    - images_folder: path to the folder containing images of the passport that need identity
                        information extraction
    - valid_mrz: Actual identity information information into the identity document. Its format is
                described below
    Example:
    valid_mrz  = {
                    "mrz_type": "TD3",
                    "type": "P",
                    "country": "CMR",
                    "number": "01312168",
                    "check_number": "4",
                    "date_of_birth": "830408",
                    "check_date_of_birth": "1",
                    "expiration_date": "140611",
                    "check_expiration_date": "5",
                    "nationality": "CMR",
                    "sex": "M",
                    "names": "ADAMOU",
                    "surname": "NCHANGE KOUOTOU"
                }
    """
    # Set the path to the folder containing images to use for the experiment
    images_folder = "data/brazil"
    # Set validation data
    valid_mrz = actual_mrz_bra
    # Run the experiment
    for i in [3,4,5,6,7]:
        print(f"\n***RESULT FOR A SAMPLE SIZE EQUAL TO {i} ***")
        unit_experiment(images_folder, valid_mrz, i)
        print('*****************************')
    
