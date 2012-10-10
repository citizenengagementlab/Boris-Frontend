from ziplookup.models import ZipCode
import os,csv

def zips(filename='zipcodes.csv'):
    f_name = os.path.abspath('boris/ziplookup/data/%s' % filename)
    csv_file = csv.DictReader(open(f_name,'rU'))
    
    i = 1
    j = 0
    for row in csv_file:
        zipcode = row['ZIPCode']
        city = row['CityName']
        state = row['StateAbbr']

        z,new = ZipCode.objects.get_or_create(zipcode=zipcode)
        z.city = city
        z.state = state

        if new:
            j += 1
            print "update",zipcode
            z.save()
        
        i+=1
    print "loaded",i,"zips"
    print j,"new"