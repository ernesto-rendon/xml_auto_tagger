# Ernesto Rendon
# June 20, 2022 10:35:01 PM
# Updated December 27, 2022 12:14:02 PM

# DECEMBER UPDATE: Script now removes Username and Password portion of the files as per new 
# standards for FTP Uploading

# Program compares all filenames in any directory & subdirectories against
# list of potential matches. If a match hits, it rewrites the file to a new,
# appropriately named .xml file, and adds appropriate XML tag to the appropriate
# location within it all saved to path of original matched file. 
# Original .xml files will be left alone. 


# These libraries import...necessary functions?
import os
import sys

# Library of keyword Filenames we're looking for, as well as database of every county's FPN code
county_codes = {
"Charlotte": "273", "Collier": "272", "Hillsborough": "275", "Lee": "271",
"Manatee": "270", "Orange": "278", "Pasco": "276", "Pinellas": "274",
"Polk": "277", "Sarasota": "134", "Flagler": "301", "Volusia": "302",
"Sarasota Observer": "408", "Longboat": "409", "East County": "410"
}
county_filenames = (
"Charlotte.xml", "Collier.xml", "Hillsborough.xml", "Lee.xml", 
"Manatee.xml", "Orange.xml", "Pasco.xml", "Pinellas.xml", "Polk.xml", 
"Sarasota.xml", "Flagler.xml", "Volusia.xml", "Sarasota Observer.xml", 
"Longboat.xml", "East County.xml"
)

# This function will handle writing of new XML file in match's directory
# Will require the PATH, NAME of matching XML file, month, day and year
def file_writer(old_file, new_location, old_county, file_month, file_day, file_year):
    
    new_file_ALPHA = os.path.join(new_location, "fpn_upload_" + county_codes[old_county] + "." + file_year + file_month + file_day + ".xml")


    # # Create new file with county code that matches name via dictionary lookup
    new_file_object = open(new_file_ALPHA, "w")


    # Open existing XML file in READ mode
    # old_file_object = open(old_file, "r")
    # Priming read for first line in existing XML file
    # old_file_line = old_file_object.readline()
    
    new_file_object.write("<xml>\n")
    new_file_object.write("  <notice>\n")
    new_file_object.write("    <subcategory_id>17</subcategory_id>\n")
    new_file_object.write("    <date>" + file_month + "/" + file_day + "/" + file_year + "</date>\n")
    new_file_object.write("    <text>Business Observer - " + old_county + " " + file_month + "/" + file_day + "/" + file_year + "</text>\n")
    new_file_object.write("    <image>" + file_year + "-" + file_month + "-" + file_day + "-" + old_county + ".pdf</image>\n")
    new_file_object.write('</notice>\n')
    new_file_object.write("</xml>\n")
    
    # old_file_object.close()
    new_file_object.close()
    
    # Confirm to user 
    print('New XML file successfully created.')

# This function handles checking of files against potential matches and initializes the publication date once per program-run
def file_checker(user_directory):

    file_month = str(raw_input("Please input the month of the publication (MM): "))
    file_day = str(raw_input("Please input the day of the publication (DD): "))
    file_year = str(raw_input("Please input the year of the publication (YYYY): "))
    
    # FILE SEARCH PARADIGM #1
    # This tries to find matches for XML files that exist in all dirs and subdirs of user provided directory
    for root, dirnames, files in os.walk(user_directory):
        for county_files in files:
            for potential_matches in county_filenames:
                if county_files == potential_matches:
                    
                    # If any file is a match against the pre-determined naming conventions, trigger a new file in that location, 
                    old_XML = os.path.join(root, county_files)
                    old_location = old_XML.rstrip(county_files)
                    old_county = county_files.rstrip(".xml")
                    
                    # Creates new directory at the root-level of user-provided folder 
                    tag_dest_folder = os.path.join(user_directory,"layouts")
                    if not os.path.exists(tag_dest_folder):
                    	os.mkdir(tag_dest_folder)
                    
                    # Function will create new XML file with ONLY the layout tag, and place it within the newly created directory
                    file_writer(old_XML, tag_dest_folder, old_county, file_month, file_day, file_year)
                    
                    # Renames the matched, extant XML file (containing individual notices) to proper encoding and leaves it in place
                    renamed_notice_XMLs = "fpn_upload_" + county_codes[old_county] + "." + file_year + file_month + file_day + ".xml"
                    final_name = os.path.join(old_location, renamed_notice_XMLs)
                    os.rename(old_XML, final_name)
  
# If number of command line arguments is less than or greater than 2, program will quit. 
# Only 1 user-provided CLI argument is necessary for program
def read_args():
    if len(sys.argv) != 2:
        print("ERROR")
        print("Usage: python -m XML_Auto_Tagger_ALPHA [directory]")
        exit()
    else:
        return{
            "live_directory": sys.argv[1]
        }

# Main function will call necessary subfunctions
def main():
    # sys.argv is a type LIST that stores input from terminal as soon as program is called in the first place
    # can be used to give program a directory to work in as soon as it's called 
    user_directory = read_args()
    if len(user_directory) == 1:
        print(str(len(user_directory)) + " directory argument detected.")
    else:
        print("Unknown error...")
        exit()    

    # Calling function that will start checking files against matches
    file_checker(user_directory["live_directory"])
    
# Start program by calling main function
main()
