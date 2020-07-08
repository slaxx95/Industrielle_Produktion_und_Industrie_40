from datetime import date
from PIL import Image
import os
import csv


TODAY = date.today()                                                # Laden des aktuellen Datums
CURRENT_DATE = TODAY.strftime("%Y_%m_%d")                           # Formatierung des Datums in die richtige Schreibweise
CURRENT_DATE = "2020_06_30"                                        # "Aktivieren" wenn ein Bild eines anderen Datums geladen werden soll


def normalize_image():                                              # Normalisierung des Kamerabilds inkl. Zuschneidung und Umwandlung in binäres Bild
    def read_image_from_disc():                                     # Laden des aktuellen Bildes
        PATH = "C:\\Users\\mathi\\Desktop\\IE40_Projekt\\Input"

        file_name = CURRENT_DATE
        input_path = PATH + "\\" + file_name + ".jpg"
        
        input_image = Image.open(input_path)
        
        return input_image


    def extract_plant_images(input_image):                          # Zuschneiden des ganzen Bildes in einzelne Bilder, die nur die Pflanzen enthalten 
        image_plant_1 = input_image.crop((1, 63, 314, 262))         # Ecke oben links: X1, Y1; Ecke unten rechts: X2, Y2
        image_plant_2 = input_image.crop((324, 63, 629, 262))
        
        return image_plant_1, image_plant_2
    
    
    def create_binary_image(image, threshold):                      # Umwandlung in ein binäres schwarz-weiß Bild mit individuell festlegbarem Threshold, um auf Belichtungsunterschiede reagieren zu können
        grayscale_image = image.convert('L')
        binary_image = grayscale_image.point(lambda p: p > threshold and 255)
        
        return binary_image
        
        
    camera_image = read_image_from_disc()
    plant_1, plant_2 = extract_plant_images(camera_image)
    plant_1_binary = create_binary_image(plant_1, 130)              # Je niedriger der Threshold, desto heller wird das Bild.
    plant_2_binary = create_binary_image(plant_2, 105)
    
    return camera_image, plant_1, plant_2, plant_1_binary, plant_2_binary



def save_images(camera_image, plant_1, plant_2, plant_1_binary, plant_2_binary):        # Benennung, Ablegung und Speicherung der einzelnen Bilder
   
    def save_image(img, name, path):
        img.save(path + "\\" + name + ".jpg", "JPEG")
    
    PATH = "C:\\Users\\mathi\\Desktop\\IE40_Projekt\\Output"
    
    directory_name = CURRENT_DATE
    
    output_path = PATH + "\\" + directory_name
    
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    save_image(camera_image, "camera", output_path)
    save_image(plant_1, "plant_1", output_path)
    save_image(plant_1_binary, "plant_1_binary", output_path)
    save_image(plant_2, "plant_2", output_path)
    save_image(plant_2_binary, "plant_2_binary", output_path)



def count_black_pixels(image):                                      # Funktion zum Zählen schwarzer Pixel
    return image.histogram()[0]                                     # Gibt den ersten Wert des Histogramm-Liste aus, welcher die schwarzen Pixel (Wert 0) zählt


def save_statistic_to_csv(count_1, count_2):                        # Speichert die Werte in einer fortlaufenden csv-Datei
    PATH = "C:\\Users\\mathi\\Desktop\\IE40_Projekt"
    csv_file = PATH + "\\" + "black_pixel_count.csv"
    
    if not os.path.isfile(csv_file):
        with open(csv_file, 'wb') as init_csvfile:
            csv.writer(init_csvfile, delimiter=',')
    
    with open(csv_file, "a", newline="") as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        spamwriter.writerow([CURRENT_DATE.replace("_", "/")] + [count_1] + [count_2])
    

cam, plant_1, plant_2, binary_1, binary_2 = normalize_image()       # Bild normalisieren
save_images(cam, plant_1, plant_2, binary_1, binary_2)              # Ursprungs- und Einzelbilder speichern
count_1 = count_black_pixels(binary_1)                              # Schwarze Pixel zählen (Pflanze 1)
count_2 = count_black_pixels(binary_2)                              # Schwarze Pixel zählen (Pflanze 2)
save_statistic_to_csv(count_1, count_2)                             # Werte in csv-Datei speichern



