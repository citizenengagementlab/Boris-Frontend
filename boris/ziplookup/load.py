from ziplookup.models import ZipCode
import os,csv

def zips(filename='zipcodes.csv'):
    f_name = os.path.abspath('boris/ziplookup/data/%s' % filename)
    csv_file = csv.DictReader(open(f_name,'rU'))
    
    i = 1
    for row in csv_file:
        z = ZipCode()
        z.zipcode = row['ZIPCODE']
        z.city = row['CITY']
        z.state = row['STATECODE']
        
        z.save()
        i+=1
    print "loaded",i,"zips"