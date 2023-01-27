# Ernesto Rendon
# June 20, 2022 10:35:01 PM

# Program compares filenames located in directories/subdirs against list of potential matches.
# If a match is found, then the match is duplicated and manipulated into a new file.
# This new dupe file is properly named, has its username/password fields removed, and is placed in the same dir as the original match.

# At the same time, another XML file is generated in a new dir on the root of the user-provided folder.
# This other XML file (solo layout file) has the same proper name as before, but only contains the single layout object 
# They need to be separated in order to have the same exact name and avoid duplicate name error


# These libraries import necessary functions
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

# This function will handle writing of new layout XML file (only containing the layout object) in the new directory, on root of user-provided directory
# Will require the PATH, NAME of matching XML file, and user-provided month, day and year
def layout_file_writer(new_location, old_county, file_month, file_day, file_year):
    
    # Open new file, which will only contain layout notice object
    solo_xml_file = os.path.join(new_location, "fpn_upload_" + county_codes[old_county] + "." + file_year + file_month + file_day + ".xml")


    # Create new file with county code that matches name via dictionary lookup
    new_solo_layout_xml = open(solo_xml_file, "w")
    
    # Write in the notice tag
    new_solo_layout_xml.write("<xml>\n")
    new_solo_layout_xml.write("  <notice>\n")
    new_solo_layout_xml.write("    <subcategory_id>17</subcategory_id>\n")
    new_solo_layout_xml.write("    <date>" + file_month + "/" + file_day + "/" + file_year + "</date>\n")
    new_solo_layout_xml.write("    <text>Business Observer - " + old_county + " " + file_month + "/" + file_day + "/" + file_year + "</text>\n")
    new_solo_layout_xml.write("    <image>" + file_year + "-" + file_month + "-" + file_day + "-" + old_county + ".pdf</image>\n")
    new_solo_layout_xml.write('</notice>\n')
    new_solo_layout_xml.write("</xml>\n")
    
    # Close the solo layout file
    new_solo_layout_xml.close()
    
    # Confirm to user 
    print('New LAYOUT XML file successfully created.')


# This function takes in old XML, and delivers a properly named copy, with the depricated username/password fields removed
def file_writer(old_file, old_location, old_county, file_month, file_day, file_year):
    

    new_file_ALPHA = os.path.join(old_location, "fpn_upload_" + county_codes[old_county] + "." + file_year + file_month + file_day + ".xml")


    # # Create new file with county code that matches name via dictionary lookup
    new_file_object = open(new_file_ALPHA, "w")


    # Open existing XML file in READ mode
    old_file_object = open(old_file, "r")
    # Priming read for first line in existing XML file
    old_file_line = old_file_object.readline()

    # While current line is NOT empty
    while old_file_line != '':
    
    	# Removing username and password portion of XML files by ignoring input and not writing to new file
    	if (old_file_line == '  <username>gulfcoast</username>\n') or (old_file_line == '  <password>legals</password>\n') or (old_file_line == '  <username>ObserverMediaGroup</username>\n'):
    		old_file_line = old_file_object.readline()
    		continue
    		
        # Copy info to NEW XML file, line by line
        new_file_object.write(old_file_line)
        old_file_line = old_file_object.readline()
    
    old_file_object.close()
    new_file_object.close()
    
    # Confirm to user 
    print('New XML file successfully created.\n')


# This function handles checking of files against potential matches and initializes the publication date once per program-run
def file_checker(user_directory):

    file_month = str(raw_input("Please input the month of the publication (MM): "))
    file_day = str(raw_input("Please input the day of the publication (DD): "))
    file_year = str(raw_input("Please input the year of the publication (YYYY): "))
    print
    
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
                    layout_file_writer(tag_dest_folder, old_county, file_month, file_day, file_year)

                    # Function will create copy of old XML file, removing the deprecated username/password tags at top of file
                    file_writer(old_XML, old_location, old_county, file_month, file_day, file_year)
  
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
