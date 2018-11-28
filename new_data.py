Supply(name="B Braun Medical Lactated Ringers 250ml", category="IV fluid", weight=0.27, image="B Braun Lactated Ringers 250ml.JPG").save()
Supply(name="ICU Medical Normosol-R Ph 7.4 500ml", category="IV fluid", weight=0.53, image="Baxter Dextrose  NaCl 1000ml.JPG").save()
Supply(name="Baxter Dextrose 5%, NaCl 0.33% 1000ml", category="IV fluid", weight=1.05, image="ICU Medical Normosol 500ml.JPG").save()

Location(name="Mui Wo General Out-patient Clinic", latitude=22.266040, longitude=113.997882, altitude=17).save()
Location(name="North Lamma General Out-patient Clinic", latitude=22.224295, longitude=114.111098, altitude=20).save()
Location(name="Peng Chau General Out-patient Clinic", latitude=22.283621, longitude=114.039154, altitude=8).save()
Location(name="Sok Kwu Wan General Out-patient Clinic", latitude=22.205606, longitude=114.131597, altitude=21).save()
Location(name="Tai O Jockey Club General Out-patient Clinic", latitude=22.255725, longitude=113.857972, altitude=2).save()
Location(name="Aberdeen Jockey Club General Out-patient Clinic", latitude=22.249740, longitude=114.156384, altitude=44).save()
Location(name="Ap Lei Chau General Out-patient Clinic", latitude=22.243243, longitude=114.153765, altitude=56).save()
Location(name="Queen Mary Hospital Drone Port", latitude=22.270257, longitude=114.131376, altitude=161).save()

DistanceBetweenLocation(location1=Location.objects.get(name="Mui Wo General Out-patient Clinic"), location2=Location.objects.get(name="North Lamma General Out-patient Clinic"), distance=12.54).save()
DistanceBetweenLocation(location1=Location.objects.get(name="Mui Wo General Out-patient Clinic"), location2=Location.objects.get(name="Peng Chau General Out-patient Clinic"), distance=4.68).save()
DistanceBetweenLocation(location1=Location.objects.get(name="Mui Wo General Out-patient Clinic"), location2=Location.objects.get(name="Sok Kwu Wan General Out-patient Clinic"), distance=15.32).save()
DistanceBetweenLocation(location1=Location.objects.get(name="Mui Wo General Out-patient Clinic"), location2=Location.objects.get(name="Tai O Jockey Club General Out-patient Clinic"), distance=14.44).save()
DistanceBetweenLocation(location1=Location.objects.get(name="Mui Wo General Out-patient Clinic"), location2=Location.objects.get(name="Aberdeen Jockey Club General Out-patient Clinic"), distance=16.41).save()
DistanceBetweenLocation(location1=Location.objects.get(name="Mui Wo General Out-patient Clinic"), location2=Location.objects.get(name="Ap Lei Chau General Out-patient Clinic"), distance=16.24).save()
DistanceBetweenLocation(location1=Location.objects.get(name="Mui Wo General Out-patient Clinic"), location2=Location.objects.get(name="Queen Mary Hospital Drone Port"), distance=13.74).save()

DistanceBetweenLocation(location1=Location.objects.get(name="North Lamma General Out-patient Clinic"), location2=Location.objects.get(name="Peng Chau General Out-patient Clinic"), distance=9.92).save()
DistanceBetweenLocation(location1=Location.objects.get(name="North Lamma General Out-patient Clinic"), location2=Location.objects.get(name="Sok Kwu Wan General Out-patient Clinic"), distance=2.96).save()
DistanceBetweenLocation(location1=Location.objects.get(name="North Lamma General Out-patient Clinic"), location2=Location.objects.get(name="Tai O Jockey Club General Out-patient Clinic"), distance=26.29).save()
DistanceBetweenLocation(location1=Location.objects.get(name="North Lamma General Out-patient Clinic"), location2=Location.objects.get(name="Aberdeen Jockey Club General Out-patient Clinic"), distance=5.45).save()
DistanceBetweenLocation(location1=Location.objects.get(name="North Lamma General Out-patient Clinic"), location2=Location.objects.get(name="Ap Lei Chau General Out-patient Clinic"), distance=4.87).save()
DistanceBetweenLocation(location1=Location.objects.get(name="North Lamma General Out-patient Clinic"), location2=Location.objects.get(name="Queen Mary Hospital Drone Port"), distance=5.52).save()


DistanceBetweenLocation(location1=Location.objects.get(name="Peng Chau General Out-patient Clinic"), location2=Location.objects.get(name="Sok Kwu Wan General Out-patient Clinic"), distance=12.88).save()
DistanceBetweenLocation(location1=Location.objects.get(name="Peng Chau General Out-patient Clinic"), location2=Location.objects.get(name="Tai O Jockey Club General Out-patient Clinic"), distance=18.90).save()
DistanceBetweenLocation(location1=Location.objects.get(name="Peng Chau General Out-patient Clinic"), location2=Location.objects.get(name="Aberdeen Jockey Club General Out-patient Clinic"), distance=12.64).save()
DistanceBetweenLocation(location1=Location.objects.get(name="Peng Chau General Out-patient Clinic"), location2=Location.objects.get(name="Ap Lei Chau General Out-patient Clinic"), distance=12.62).save()
DistanceBetweenLocation(location1=Location.objects.get(name="Peng Chau General Out-patient Clinic"), location2=Location.objects.get(name="Queen Mary Hospital Drone Port"), distance=9.61).save()

DistanceBetweenLocation(location1=Location.objects.get(name="Sok Kwu Wan General Out-patient Clinic"), location2=Location.objects.get(name="Tai O Jockey Club General Out-patient Clinic"), distance=28.71).save()
DistanceBetweenLocation(location1=Location.objects.get(name="Sok Kwu Wan General Out-patient Clinic"), location2=Location.objects.get(name="Aberdeen Jockey Club General Out-patient Clinic"), distance=5.53).save()
DistanceBetweenLocation(location1=Location.objects.get(name="Sok Kwu Wan General Out-patient Clinic"), location2=Location.objects.get(name="Ap Lei Chau General Out-patient Clinic"), distance=4.77).save()
DistanceBetweenLocation(location1=Location.objects.get(name="Sok Kwu Wan General Out-patient Clinic"), location2=Location.objects.get(name="Queen Mary Hospital Drone Port"), distance=7.19).save()

DistanceBetweenLocation(location1=Location.objects.get(name="Tai O Jockey Club General Out-patient Clinic"), location2=Location.objects.get(name="Aberdeen Jockey Club General Out-patient Clinic"), distance=30.72).save()
DistanceBetweenLocation(location1=Location.objects.get(name="Tai O Jockey Club General Out-patient Clinic"), location2=Location.objects.get(name="Ap Lei Chau General Out-patient Clinic"), distance=30.47).save()
DistanceBetweenLocation(location1=Location.objects.get(name="Tai O Jockey Club General Out-patient Clinic"), location2=Location.objects.get(name="Queen Mary Hospital Drone Port"), distance=28.18).save()

DistanceBetweenLocation(location1=Location.objects.get(name="Aberdeen Jockey Club General Out-patient Clinic"), location2=Location.objects.get(name="Ap Lei Chau General Out-patient Clinic"), distance=0.77).save()
DistanceBetweenLocation(location1=Location.objects.get(name="Aberdeen Jockey Club General Out-patient Clinic"), location2=Location.objects.get(name="Queen Mary Hospital Drone Port"), distance=3.44).save()

DistanceBetweenLocation(location1=Location.objects.get(name="Ap Lei Chau General Out-patient Clinic"), location2=Location.objects.get(name="Queen Mary Hospital Drone Port"), distance=3.79).save()
