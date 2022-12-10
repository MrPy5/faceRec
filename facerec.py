import time
from PIL import Image, ImageDraw
import face_recognition
import os
while True:
    while True:
        bestmatch = -1
        reportstrue = False
        moreinfo = ""
        countedoff = 0
        b2 = 0
        x2 = 0
        noerror = True
        imagetoshow = 0
        print("What do you want to do: ")
        print("> edit file, ")
        print("> new file, ")
        print("> compare faces with face cache, ")
        print("> take picture to compare with face cache")
        whattodo = input("edit/new/compare/camera ")
        if whattodo.lower() == "compare" or whattodo.lower() == "camera":
            ended = False
            descriptionfiles = []
            if whattodo.lower() == "compare": 
                file = input("What file do you want to compare with the face cache? ")
            if whattodo.lower() == "camera":
                import pygame
                import pygame.camera
                pygame.camera.init()
     #Camera detected or not
                cam = pygame.camera.Camera("/dev/video0",(640,480))
                cam.start()
                input("Press enter to take picture")
                

                img = cam.get_image()
                filesaveasname = input("What name would you like this file to be saved under? ")
                for x in os.listdir("/home/pi/Face_rec"):
                    if x[x.find(".")] == filesaveasname:
                        noerror = False
                if noerror == True:
                    pygame.image.save(img, "/home/pi/Face_rec/" + filesaveasname + ".jpg")
                    cam.stop()
                    print("Saving...")
                    time.sleep(3)
                    print("Saved!")
                    file = filesaveasname + ".jpg"
                    print(file)
                else:
                    print("Name already taken :(")
            face_number = 0



            try:
                unknown_picture = face_recognition.load_image_file("/home/pi/Face_rec/" + file)
                unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]
                picture_of_me = face_recognition.load_image_file("/home/pi/Face_rec/donald.jpeg")
                my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]
            
            except:
                print("There has been an error, you might have done one of the following:")
                print("> Incorrect image name")
                print("> No faces in photo")
                print("> The photo is blurry")
                print("Please try again with a new image")
            
                break   


            pil_image = Image.fromarray(unknown_picture)

            pil_image.show()

            faces = []
            for x in os.listdir("/home/pi/python/faces"):
                if x not in faces:
                    faces.append(x)
            for x in os.listdir("/home/pi/python/description"):
                if x not in descriptionfiles:
                    descriptionfiles.append(x)
            face_locations = face_recognition.face_locations(unknown_picture)
            all = True
            reports = False
            for face_location in face_locations:
            

            
                unknown_picture = face_recognition.load_image_file("/home/pi/Face_rec/" + file)
                unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[face_number]
            
            
                top, right, bottom, left = face_location
                

            
                face_image = unknown_picture[top:bottom, left:right]
                pil_image = Image.fromarray(face_image)
                pil_image.show()
                where_dot = file.find(".")
                new_image = file[:where_dot] + str(face_number + 1) + ".jpg"
                descriptionfile = file[:where_dot] + str(face_number + 1) + ".txt"
            
            #new_image = f'{top,right,bottom,left}' + ".jpg"
                
                new_image_file = "/home/pi/python/faces/" + new_image
                pil_image.save(new_image_file)
                
                if descriptionfile not in descriptionfiles:
                    writefile = input("Would you like to write a small report on this face? y/n ")
                    if writefile.lower() == "y":
                        newfileopen = open("/home/pi/python/description/" + descriptionfile, "w+")
                        init = input("What would you like the file to say? ")
                        newfileopen.write(init)
                        newfileopen.close()
                    
            
                choosereports = input("Would you like to see all faces or just the ones with reports? all/reports ")
                if choosereports.lower() == "reports":
                    reports = True
                    allorsome = input("Would you like to see all faces with reports or the best hit with reports? all/best ")
                    if allorsome.lower() == "all":
                        all = True
                    else:
                        all = False
                if choosereports.lower() == "all":
                    reports = False
                    allorsome = input("Would you like to see all faces or the best hit? all/best ")
                    if allorsome.lower() == "all":
                        all = True
                    else:
                        all = False

                for x in faces:
                    
                    if ended == True:
                        ended = False
                        break
                    try:
                
                        picture_of_me = face_recognition.load_image_file("/home/pi/python/faces/%s" % x)
                        my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]
                 
                    
                    
                    
                    
                    
                        results = face_recognition.compare_faces([my_face_encoding], unknown_face_encoding)
                    
                    
                        if results[0] == True:
                            if reports == True:
                                remembered_image = "/home/pi/python/faces/" + x
                                remembered_file = face_recognition.load_image_file(remembered_image)
                                pil_image = Image.fromarray(remembered_file)
                                for b in os.listdir("/home/pi/python/description"):
                                        
                                    if "/home/pi/python/faces/" + new_image != remembered_image and x[:x.find(".")] == b[:b.find(".")]:
                                        face_distances = face_recognition.face_distance([my_face_encoding], unknown_face_encoding)

                                        percent = face_distances
                                            
                                        percent2 = str(percent).replace("[", "").replace("]", "").replace(".", "")
                                        percent2 = percent2[percent2.find("0") + 1:]
                                        if all != False:
                                            print(str(100 - int(percent2[:2])) + "% Match. Aim for 40 - 50")
                                        if 100 - int(percent2[:2]) > bestmatch:
                                            bestmatch = 100 - int(percent2[:2])
                                            reportstrue = reports
                                            moreinfo = str(face_number+1)
                                            b2 = b
                                            x2 = x
                                            imagetoshow = Image.fromarray(remembered_file)
                                        if all != False:
                                            pil_image.show()
                                        
                                            print("I remember the " + str(face_number+1)+ " face from the image " + x)
                                            
                                            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                                            print("Here is some information I pulled up which can be found at " + b)
                                                    
                                            fileopen = open("/home/pi/python/description/" + b, "r")
                                            print(fileopen.read())
                                            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                                            break
                
                                            
                                            
                                            
                                        
                            if reports == False:
                                remembered_image = "/home/pi/python/faces/" + x
                                remembered_file = face_recognition.load_image_file(remembered_image)
                                pil_image = Image.fromarray(remembered_file)
                                
                                if 6 == 6:        
                                    if "/home/pi/python/faces/" + new_image != remembered_image:
                                        
                                    
                                       
                                        face_distances = face_recognition.face_distance([my_face_encoding], unknown_face_encoding)
                                        percent = face_distances
                                        
                                        percent2 = str(percent).replace("[", "").replace("]", "").replace(".", "")
                                        percent2 = percent2[percent2.find("0") + 1:]
                                        if all != False:
                                            pil_image.show()
                                                                                   
                                        
                                            print("I remember the " + str(face_number+1)+ " face from the image " + x)
                                            print(str(100 - int(percent2[:2])) + "% Match. Aim for 40 - 50")
                                        if 100 - int(percent2[:2]) > bestmatch:
                                            bestmatch = 100 - int(percent2[:2])
                                            reportstrue = reports
                                            moreinfo = str(face_number+1)
                                                
                                            x2 = x
                                            imagetoshow = Image.fromarray(remembered_file)
                                        for b in os.listdir("/home/pi/python/description"):
                                            if x[:x.find(".")] == b[:b.find(".")]:
                                                b2 = b
                                                reportstrue = True
                                            if all != False and x[:x.find(".")] == b[:b.find(".")]:

                                            
                                                print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                                                print("Here is some information I pulled up which can be found at " + b)
                                                    
                                                fileopen = open("/home/pi/python/description/" + b, "r")
                                                print(fileopen.read())
                                                print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                                                break
                                            
                                        
                                    
                            
                                
                    except:
                        pass
                    
                if all != True and bestmatch != -1 and reports == True:
                    
                    if reportstrue == True:
                        imagetoshow.show()
                        print("This is the best match I could find: ")
                        print(str(100 - int(percent2[:2])) + "% Match. Aim for 40 - 50")
                        print("I remember the " + moreinfo + " face from the image " + x2)
                        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                        print("Here is some information I pulled up which can be found at " + b2)
                                                        
                        fileopen = open("/home/pi/python/description/" + b2, "r")
                        print(fileopen.read())
                        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                if all != True and bestmatch != -1 and reports == False:
                    imagetoshow.show()
                    print("This is the best match I could find: ")
                    print(str(100 - int(percent2[:2])) + "% Match. Aim for 40 - 50")
                    print("I remember the " + moreinfo + " face from the image " + x2)
                    if reportstrue == True:
                        
                        
                        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                        print("Here is some information I pulled up which can be found at " + b2)
                                                        
                        fileopen = open("/home/pi/python/description/" + b2, "r")
                        print(fileopen.read())
                        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
               
                    


                face_number+=1
        if whattodo.lower() == "edit":
            name = input("What face names file do you want to edit? or C to cancel ")
            if name != "C":
                for b in os.listdir("/home/pi/python/description"):
                    filenameopens = open("/home/pi/python/description/" + b, "r")
                    filenameopenss = open("/home/pi/python/description/" + b, "r")
                    line = filenameopens.readlines()
                    
                    for q in line:
                      
                      countedoff += 1
                      if countedoff != -1:
                        if q.strip().lower() == name.strip().lower():
                            print("Here is what the old file said named " + b)
                            print(filenameopenss.read())
                            newfilesays = input("Type what the new file will say. Use \' > \' for new line or use C to cancel ")
                            if newfilesays != "C":
                                filenameopensss = open("/home/pi/python/description/" + b, "w")
                                newfilesays = newfilesays.replace(" > ", "\n")
                                filenameopensss.write(newfilesays)
                                filenameopensss.close()
        
                    

                filenameopens.close()
                filenameopenss.close()
        if whattodo.lower() == "new":
            nameoffile = input("What is the name of the file that you want to be created that can be associated with a face? (filename + face number) ")
            for b in os.listdir("/home/pi/python/faces"):
                if b[:b.find(".")] == nameoffile:
                    
                    print("I have found your face!")
                    newfilesays = input("Type what the new file will say. Use \' > \' for new line ")
                    filenameopensss = open("/home/pi/python/description/" + b, "w")
                    newfilesays = newfilesays.replace(" > ", "\n")
                    filenameopensss.write(newfilesays)
                    filenameopensss.close()

