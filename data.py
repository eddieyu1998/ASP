from ASP.models import *

ClinicManager(firstName="Manager", lastName="1", password="manager1", email="manager1@ha.org").save()
ClinicManager(firstName="Manager", lastName="2", password="manager2", email="manager2@ha.org").save()
ClinicManager(firstName="Manager", lastName="3", password="manager3", email="manager3@ha.org").save()
ClinicManager(firstName="Manager", lastName="4", password="manager4", email="manager4@ha.org").save()
ClinicManager(firstName="Manager", lastName="5", password="manager5", email="manager5@ha.org").save()
ClinicManager(firstName="Manager", lastName="6", password="manager6", email="manager6@ha.org").save()
ClinicManager(firstName="Manager", lastName="7", password="manager7", email="manager7@ha.org").save()
ClinicManager(firstName="Health", lastName="Authority", password="ha", email="ha@ha.org").save()

Clinic(manager=ClinicManager.objects.get(pk=1), name="Mui Wo General Out-patient Clinic", latitude=22.266040, longitude=113.997882, altitude=17).save()
Clinic(manager=ClinicManager.objects.get(pk=2), name="North Lamma General Out-patient Clinic", latitude=22.224295, longitude=114.111098, altitude=20).save()
Clinic(manager=ClinicManager.objects.get(pk=3), name="Peng Chau General Out-patient Clinic", latitude=22.283621, longitude=114.039154, altitude=8).save()
Clinic(manager=ClinicManager.objects.get(pk=4), name="Sok Kwu Wan General Out-patient Clinic", latitude=22.205606, longitude=114.131597, altitude=21).save()
Clinic(manager=ClinicManager.objects.get(pk=5), name="Tai O Jockey Club General Out-patient Clinic", latitude=22.255725, longitude=113.857972, altitude=2).save()
Clinic(manager=ClinicManager.objects.get(pk=6), name="Aberdeen Jockey Club General Out-patient Clinic", latitude=22.249740, longitude=114.156384, altitude=44).save()
Clinic(manager=ClinicManager.objects.get(pk=7), name="Ap Lei Chau General Out-patient Clinic", latitude=22.243243, longitude=114.153765, altitude=56).save()
Clinic(manager=ClinicManager.objects.get(pk=8), name="Queen Mary Hospital Drone Port", latitude=22.270257, longitude=114.131376, altitude=161).save()

DistanceBetweenClinic(clinic1=Clinic.objects.get(pk=1), clinic2=Clinic.objects.get(pk=2), distance=12.54).save()
DistanceBetweenClinic(clinic1=Clinic.objects.get(pk=1), clinic2=Clinic.objects.get(pk=3), distance=4.68).save()
DistanceBetweenClinic(clinic1=Clinic.objects.get(pk=1), clinic2=Clinic.objects.get(pk=4), distance=15.32).save()
DistanceBetweenClinic(clinic1=Clinic.objects.get(pk=1), clinic2=Clinic.objects.get(pk=5), distance=14.44).save()
DistanceBetweenClinic(clinic1=Clinic.objects.get(pk=1), clinic2=Clinic.objects.get(pk=6), distance=16.41).save()
DistanceBetweenClinic(clinic1=Clinic.objects.get(pk=1), clinic2=Clinic.objects.get(pk=7), distance=16.24).save()
DistanceBetweenClinic(clinic1=Clinic.objects.get(pk=1), clinic2=Clinic.objects.get(pk=8), distance=13.74).save()

DistanceBetweenClinic(clinic1=Clinic.objects.get(pk=2), clinic2=Clinic.objects.get(pk=3), distance=9.92).save()
DistanceBetweenClinic(clinic1=Clinic.objects.get(pk=2), clinic2=Clinic.objects.get(pk=4), distance=2.96).save()
DistanceBetweenClinic(clinic1=Clinic.objects.get(pk=2), clinic2=Clinic.objects.get(pk=5), distance=26.29).save()
DistanceBetweenClinic(clinic1=Clinic.objects.get(pk=2), clinic2=Clinic.objects.get(pk=6), distance=5.45).save()
DistanceBetweenClinic(clinic1=Clinic.objects.get(pk=2), clinic2=Clinic.objects.get(pk=7), distance=4.87).save()
DistanceBetweenClinic(clinic1=Clinic.objects.get(pk=2), clinic2=Clinic.objects.get(pk=8), distance=5.52).save()


DistanceBetweenClinic(clinic1=Clinic.objects.get(pk=3), clinic2=Clinic.objects.get(pk=4), distance=12.88).save()
DistanceBetweenClinic(clinic1=Clinic.objects.get(pk=3), clinic2=Clinic.objects.get(pk=5), distance=18.90).save()
DistanceBetweenClinic(clinic1=Clinic.objects.get(pk=3), clinic2=Clinic.objects.get(pk=6), distance=12.64).save()
DistanceBetweenClinic(clinic1=Clinic.objects.get(pk=3), clinic2=Clinic.objects.get(pk=7), distance=12.62).save()
DistanceBetweenClinic(clinic1=Clinic.objects.get(pk=3), clinic2=Clinic.objects.get(pk=8), distance=9.61).save()

DistanceBetweenClinic(clinic1=Clinic.objects.get(pk=4), clinic2=Clinic.objects.get(pk=5), distance=28.71).save()
DistanceBetweenClinic(clinic1=Clinic.objects.get(pk=4), clinic2=Clinic.objects.get(pk=6), distance=5.53).save()
DistanceBetweenClinic(clinic1=Clinic.objects.get(pk=4), clinic2=Clinic.objects.get(pk=7), distance=4.77).save()
DistanceBetweenClinic(clinic1=Clinic.objects.get(pk=4), clinic2=Clinic.objects.get(pk=8), distance=7.19).save()

DistanceBetweenClinic(clinic1=Clinic.objects.get(pk=5), clinic2=Clinic.objects.get(pk=6), distance=30.72).save()
DistanceBetweenClinic(clinic1=Clinic.objects.get(pk=5), clinic2=Clinic.objects.get(pk=7), distance=30.47).save()
DistanceBetweenClinic(clinic1=Clinic.objects.get(pk=5), clinic2=Clinic.objects.get(pk=8), distance=28.18).save()

DistanceBetweenClinic(clinic1=Clinic.objects.get(pk=6), clinic2=Clinic.objects.get(pk=7), distance=0.77).save()
DistanceBetweenClinic(clinic1=Clinic.objects.get(pk=6), clinic2=Clinic.objects.get(pk=8), distance=3.44).save()

DistanceBetweenClinic(clinic1=Clinic.objects.get(pk=7), clinic2=Clinic.objects.get(pk=8), distance=3.79).save()

Supply(name="B Braun Medical Lactated Ringers 250ml", category="IV fluid", weight=0.27, image="B Braun Lactated Ringers 250ml.JPG").save()
Supply(name="ICU Medical Normosol-R Ph 7.4 500ml", category="IV fluid", weight=0.53, image="Baxter Dextrose  NaCl 1000ml.JPG").save()
Supply(name="Baxter Dextrose 5%, NaCl 0.33% 1000ml", category="IV fluid", weight=1.05, image="ICU Medical Normosol 500ml.JPG").save()