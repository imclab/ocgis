import unittest
from netCDF4 import Dataset
from ocgis.interface.projection import get_projection
from ocgis import Inspect
from ocgis.api.operations import OcgOperations
from ocgis.api.dataset.request import RequestDataset
from ocgis.test.base import TestBase


class Test(TestBase):
    
    def setUp(self):
#        self.hostetler = self.test_data.get_rd('hostetler').uri
        self.daymet = self.test_data.get_rd('daymet_tmax').uri
    
    def test_get_projection(self):
        ip = Inspect(self.daymet,variable='tmax')
        ip.__repr__()
        
        ds = Dataset(self.daymet)
        proj = get_projection(ds)
        self.assertEqual(proj.sr.ExportToProj4(),
         '+proj=lcc +lat_1=25 +lat_2=60 +lat_0=42.5 +lon_0=-100 +x_0=0 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs ')
        
    def test_daymet(self):
#        uri = 'http://daymet.ornl.gov/thredds//dodsC/allcf/2011/9947_2011/tmax.nc'
        rd = self.test_data.get_rd('daymet_tmax')
        geom = 'state_boundaries'
        select_ugid = [32]
        snippet = True
        ops = OcgOperations(dataset=rd,geom=geom,snippet=snippet,
         select_ugid=select_ugid,output_format='numpy')
        ops.execute()
        
    def test_differing_projections(self):
        rd1 = self.test_data.get_rd('daymet_tmax')
#        rd2 = RequestDataset(uri=self.hostetler,variable='TG',t_calendar='noleap')
        rd2 = self.test_data.get_rd('cancm4_tas')
        ops = OcgOperations(dataset=[rd1,rd2],snippet=True)
        with self.assertRaises(ValueError):
            ops.execute()
            
    def test_same_projection(self):
        daymet_uri = self.test_data.get_rd('daymet_tmax').uri
        rd1 = RequestDataset(uri=daymet_uri,variable='tmax',alias='tmax1')
        rd2 = RequestDataset(uri=daymet_uri,variable='tmax',alias='tmax2')
        ops = OcgOperations(dataset=[rd1,rd2],snippet=True)
        ops.execute()


if __name__ == "__main__":
#    import sys;sys.argv = ['', 'TestSimpleMultiCalc01.test']
    unittest.main()