from django.test import TestCase
from django.test.client import Client
from climatedata.models import NetcdfDataset
import unittest
import itertools
import pdb
from util.helpers import reverse_wkt


#def disabled(f):
#    warn('{0} TEST DISABLED!'.format(f.__name__))

#class TestViews(TestCase):
#    
#    fixtures = ['test_usgs-cida-maurer.json']
#    
#    def test_get_choices(self):
#        choices = get_choices(Archive)
#        self.assertEqual(len(choices),2)
#        
#        choices = get_choices(SimulationOutput,'pk','run',True)
#        self.assertEqual(len(choices),3)
    

class TestUrls(TestCase):
    """Test URLs for correct response codes."""
    
#    fixtures = ['luca_fixtures.json']
    fixtures = ['test_usgs-cida-maurer.json']
    
    def setUp(self):
        self.client = Client()
    
    def test_fixture_loading(self):
        '''Check that the test fixture loaded correctly'''
        self.assertEqual(NetcdfDataset.objects.count(), 1)
    
    def test_api_html(self):
        '''Creates an HTML representation of the API main page'''
        response = self.client.get('/api/')
        if response.status_code != 200:
                print response.content
        self.assertEqual(response.status_code, 200)

    def test_api_urls(self):
        '''tests a combination of resources and formats'''
        resources = [
            '/api/archives',
            '/api/archives/usgs-cida-maurer',
            '/api/scenarios',
            '/api/scenarios/sres-a1b',
            '/api/models',
            '/api/models/echam5-mpi-om',
            '/api/variables',
            '/api/variables/pr',
            '/api/simulations',
            '/api/simulations/1',
        ]
        suffixes = [
            '',
            '/',
            '.html',
            '.json',
        ]
        for resource in resources:
            for suffix in suffixes:
                print 'testing: {0}{1}'.format(resource,suffix)
                response = self.client.get('{0}{1}'.format(resource,suffix))
                if response.status_code != 200:
                    print response.content
                self.assertEqual(response.status_code, 200)
    
    def test_data_request_urls(self):
        '''tests that data request URLs work
        
        This tests many different combinations of:
        * output formats (CSV, Shapefile, GeoJSON)
        * spatial operations (intersects or clip)
        * aggregation
        '''
        exts = [
#            'csv',
            'kcsv',
#            'shz',
#            'geojson',
        ]
        drange = '2010-3-1+2010-4-30'
        polygon = '-96.25+38.7,-95.78+38.1,-95.9+39.1,-96.23+39.8,-96.25+38.7'
        sops = [
            'intersects',
#            'clip',
        ]
        aggs = [
            'true',
#            'false',
        ]
        cm = 'miroc3.2(medres)'
        scenario = 'sres-a1b'
        archive = 'usgs-cida-maurer'
        var = 'pr'
        run = 2
        
        for ext,sop,agg in itertools.product(exts,sops,aggs):
            
            print(ext,sop,agg)
        
            base_url = ('/api'
                        '/archive/{archive}/model'
                        '/{cm}/scenario/{scenario}'
                        '/run/{run}'
                        '/temporal/{drange}'
                        '/spatial/{sop}+polygon(({polygon}))'
                        '/aggregate/{agg}'
                        '/variable/{variable}.{ext}')
            
            url = base_url.format(ext=ext,
                                  drange=drange,
                                  polygon=polygon,
                                  sop=sop,
                                  agg=agg,
                                  cm=cm,
                                  scenario=scenario,
                                  archive=archive,
                                  variable=var,
                                  run=run)

            response = self.client.get(url)
#            if response.status_code != 200:
#                print response.content
            self.assertEqual(response.status_code, 200)
    
    def test_simple_json_data_request(self):
        '''tests that a simple data request URLs works'''
    
        url = ('/api'
               '/archive/{archive}'
               '/model/{cm}'
               '/scenario/{scenario}'
               '/run/{run}'
               '/temporal/{drange}'
               '/spatial/{sop}+polygon(({polygon}))'
               '/aggregate/{agg}'
               '/variable/{variable}.{ext}'
               ).format(ext='json',
                        drange='2000-01-01+2000-02-01',
                        polygon='-104+39.75,-103.75+39.75,-103.75+40,-104+39.75',
                        sop='intersects',
                        agg='false',
                        cm='miroc3.2(medres)',
                        scenario='sres-a1b',
                        archive='usgs-cida-maurer',
                        variable='pr',
                        run=2,
                )
        response = self.client.get(url)
        if response.status_code != 200:
            print response.content
        self.assertEqual(response.status_code, 200)
    
    def test_simple_kml_data_request(self):
        '''tests that a simple KML data request works'''
    
        url = ('/api'
               '/archive/{archive}'
               '/model/{cm}'
               '/scenario/{scenario}'
               '/run/{run}'
               '/temporal/{drange}'
               '/spatial/{sop}+polygon(({polygon}))'
               '/aggregate/{agg}'
               '/variable/{variable}.{ext}'
               ).format(
                    ext='kml',
                    drange='2000-01-01+2000-02-01',
                    polygon='-104+39.75,-103.75+39.75,-103.75+40,-104+39.75',
                    sop='intersects',
                    agg='false',
                    cm='miroc3.2(medres)',
                    scenario='sres-a1b',
                    archive='usgs-cida-maurer',
                    variable='pr',
                    run=2,
                )
        response = self.client.get(url)
        if response.status_code != 200:
            print response.content
        self.assertEqual(response.status_code, 200)

    def test_simple_kmz_data_request(self):
        '''tests that a simple KMZ data request works'''
        
        url = ('/api'
               '/archive/{archive}'
               '/model/{cm}'
               '/scenario/{scenario}'
               '/run/{run}'
               '/temporal/{drange}'
               '/spatial/{sop}+polygon(({polygon}))'
               '/aggregate/{agg}'
               '/variable/{variable}.{ext}'
               ).format(
                    ext='kmz',
                    drange='2000-01-01+2000-02-01',
                    polygon='-104+39.75,-103.75+39.75,-103.75+40,-104+39.75',
                    sop='intersects',
                    agg='false',
                    cm='miroc3.2(medres)',
                    scenario='sres-a1b',
                    archive='usgs-cida-maurer',
                    variable='pr',
                    run=2,
                )
        response = self.client.get(url)
        if response.status_code != 200:
            print response.content
        self.assertEqual(response.status_code, 200)
    
    
    def test_simple_kmz_data_request_detroit(self):
        '''tests that a KMZ data request for the detroit area works'''
        
        poly = 'POLYGON ((-83.142128872393371 42.22762950293189,-83.142128872393371 42.22762950293189,-83.142128872393371 42.22762950293189,-83.17525346549246 42.146264960288335,-83.183237474281555 42.10817942968923,-83.206207648435296 42.098877671876693,-83.298992682615363 42.090066840170934,-83.311834276039889 42.127997341473161,-83.311679246743012 42.178976141929098,-83.537324388345468 42.207346503257341,-83.781598883789158 42.217061672528203,-83.811958787760631 42.256542466799203,-83.819684414388263 42.31865753841403,-83.721783413411316 42.330181382815113,-83.629179246744286 42.280572007814925,-83.565022956053923 42.279900214195123,-83.514896816730811 42.293258571942573,-83.536626756509534 42.417592068036825,-83.578381313801373 42.521849270185683,-83.510788540363592 42.634555569014253,-83.48949785025934 42.76317820898872,-83.414722052732998 42.774960435551279,-83.349790615558263 42.750465806644925,-83.301369798500787 42.784572251957556,-83.273593716143893 42.839349270186943,-83.25641130240686 42.837488918624445,-83.24819474967245 42.826662706059295,-83.221271328448381 42.790075791996642,-83.210083380857185 42.737753404301131,-83.056139289059701 42.732947496097978,-82.943381313798824 42.686955471358218,-82.887648281572041 42.689048366866032,-82.828091193355661 42.698866889001494,-82.808299119787875 42.684009914717578,-82.790083177404995 42.665148016931042,-82.787835252600289 42.663830267907599,-82.804423387365972 42.63892222754292,-82.783804490881522 42.612722276370931,-82.796000128902406 42.589131985029695,-82.840958624996333 42.568099677086906,-82.870104132808947 42.519007066409628,-82.883384975907973 42.441854152997863,-82.902014329749193 42.394001776695589,-82.925992194332622 42.375501613935086,-83.016503465491837 42.347131252606857,-83.063373989580555 42.32266246191665,-83.104818488278639 42.286437282880044,-83.142128872393371 42.22762950293189))'
        url = ('/api'
               '/archive/{archive}'
               '/model/{cm}'
               '/scenario/{scenario}'
               '/run/{run}'
               '/temporal/{drange}'
               '/spatial/{sop}+{polygon}'
               '/aggregate/{agg}'
               '/variable/{variable}.{ext}'
               ).format(
                    ext='shz',
                    drange='2000-01-01+2000-02-01',
                    polygon=reverse_wkt(poly),
                    sop='clip',
                    agg='false',
                    cm='miroc3.2(medres)',
                    scenario='sres-a1b',
                    archive='usgs-cida-maurer',
                    variable='pr',
                    run=2,
                )
        response = self.client.get(url)
        if response.status_code != 200:
            print response.content
        self.assertEqual(response.status_code, 200)
    
    
    def test_clip_of_nonaggregated_geometries(self):
        '''tests that clipped geometries differ from intersected geometries
        for non-aggregated geometries
        '''
        from lxml import etree
        
        url_template = (
            '/api'
            '/archive/usgs-cida-maurer'
            '/model/miroc3.2(medres)'
            '/scenario/sres-a1b'
            '/run/2'
            '/temporal/2000-01-01+2000-02-01'
            '/spatial/{operation}+polygon((-104+39,+-103+39,+-103+40,+-104+39))'
            '/aggregate/false'
            '/variable/pr.kml'
        )
        url_clip = url_template.format(operation='clip')
        response_clip = self.client.get(url_clip)
        doc_clip = etree.fromstring(response_clip.content)
        folder_kml_string_clip = etree.tostring(
            doc_clip.find('.//{http://www.opengis.net/kml/2.2}Folder')
        )
        
        url_intersects = url_template.format(operation='intersects')
        response_intersects = self.client.get(url_intersects)
        doc_intersects = etree.fromstring(response_intersects.content)
        folder_kml_string_intersects = etree.tostring(
            doc_intersects.find('.//{http://www.opengis.net/kml/2.2}Folder')
        )
        self.assertNotEqual(
            folder_kml_string_clip,
            folder_kml_string_intersects
        )
    
    def test_query_form(self):
        '''Creates a query form'''
        response = self.client.get(
            '/api'
            '/archive/usgs-cida-maurer'
            '/model/ccsm3'
            '/scenario/sres-b1'
            '/variable/tas'
            '/run/2'
            '/query.html'
        )
        if response.status_code != 200:
                print response.content
        self.assertEqual(response.status_code, 200)
    
#    def OLD_test_urls(self):
#
#        ## list of extensions to test
#        exts = [
#                'shz',
#                'geojson',
#                'json',
#                'html'
#                ]
#        ## date ranges to test
#        dranges = [
#                   '2011-2-15',
#                   '2011-01-16+2011-3-16',
#                   ]
#        ## polygons intersections to test
#        polygons = [
##                    '11.5+3.5,12.5+3.5,12.5+2.5,11.5+2.5',
##                    '10.481+5.211,10.353+0.698,13.421+1.533,13.159+4.198',
#                    '18.746123371481431+80.295526668209391,18.261118856852192+82.963051498670211,0.073449558255717+86.358083101074868,36.206285898134041+86.843087615704121,66.5190680624615+81.023033440153256,106.531940519373734+64.532879942759109,181.707640286905814+82.478046984040958,205.715363761053169+65.017884457388362,280.163556756641356+78.598010867007048,288.651135762653098+47.557721930735738,293.986185423574739+70.110431860995362,294.956194452833188+49.982744503881918,302.23126217227184+74.717974749973138,300.291244113754829+43.192681299072575,355.824261038802774+86.358083101074868,356.551767810746583+-86.061021849619692,225.35804660353736+-83.150994761844245,145.089799432398252+-19.857905602728522,106.774442776688346+-54.778230656033756,93.436818624384273+-38.045574901324997,59.001498085708292+-80.483469931383439,22.626159488515341+-77.33094058629338,10.258544365469746+-69.328366094910933,22.868661745829968+-31.25551169651564,24.808679804346923+8.272356245767355,10.986051137413604+33.4925910064878,18.746123371481431+80.295526668209391',
#                    '71.009248245704413+28.048816528798497,84.841541328399558+26.255741499560216,87.40307708445421+14.984984172919738,82.792312723555824+7.300376904755765,73.826937577364532+5.763455451122965,64.09310170435684+9.093451933994018,63.836948128751374+20.364209260634524',
#                    ]
#        ## spatial operations
#        sops = [
#                'intersects',
#                'clip'
#                ]
#        ## aggregation
#        aggs = [
#                'true',
#                'false'
#                ]
#        ## climate models
#        cms = [
#               'bccr-bcm2.0'
#               ]
#        ## scenarios
#        scenarios = [
#                     '1pctto2x',
#                     ]
#        ## archives
#        archives = [
#                    'cmip3',
#                    ]
#        ## variables
#        variables = [
#                     'ps',
#                     ]
#        
#        base_url = ('/api/archive/{archive}/model/{cm}/scenario/{scenario}/'
#                    'temporal/{drange}/spatial/{sop}+polygon'
#                    '(({polygon}))/aggregate/{agg}/'
#                    'variable/{variable}.{ext}')
#        
##        for ext,drange,polygon,sop,agg,cm,scenario,archive,variable in itertools.product(exts,dranges,polygons,sops,aggs,cms,scenarios,archives,variables):
##            print ext,drange,'polygon index: '+str(polygons.index(polygon)),sop,agg,cm,scenario,archive,variable,'\n'
##            url = base_url.format(ext=ext,drange=drange,polygon=polygon,sop=sop,agg=agg,cm=cm,scenario=scenario,archive=archive,variable=variable)
##            response = self.client.get(url)
##            self.assertTrue(response.content != None)
##            self.assertEqual(response.status_code,200)
#
#        dranges = [
##                   '1950-5-15',
#                   '1950-9-1+1951-11-30'
#                   ]
#        polygons = [
#                    '-105.810709477731606+41.745763941079858,-104.480587924505272+41.72442509263238,-104.480587924505272+41.72442509263238,-103.634146936088499+41.639069698842455,-102.816157745601714+42.179653859511987,-101.279760657383051+42.641995575874084,-100.703611749301047+42.421494141916774,-100.390641972071322+41.994717172967142,-100.710724698783537+41.361664669025195,-101.407793748067931+40.586353175433366,-103.207369967138874+39.988865418903892,-103.925777864870753+39.66878269219167,-105.206108771719627+39.298909319101988,-106.60735981977092+39.462507157199347,-106.806522405280745+40.337399943546089,-106.642924567183385+41.240744527822798,-105.810709477731606+41.745763941079858',
#                    ]
#        archives = [
#                    'maurer07'
#                    ]
#        cms = [
#               'bccr-bcm2.0',
#               'cccma-cgcm3.1'
#               ]
#        scenarios = [
#                     'sresa1b',
#                     'sresa2'
#                     ]
#        variables = [
#                     'Prcp',
#                     ]
#        
#        for ext,drange,polygon,sop,agg,cm,scenario,archive,variable in itertools.product(exts,dranges,polygons,sops,aggs,cms,scenarios,archives,variables):
#            print ext,drange,'polygon index: '+str(polygons.index(polygon)),sop,agg,cm,scenario,archive,variable,'\n'
#            url = base_url.format(ext=ext,drange=drange,polygon=polygon,sop=sop,agg=agg,cm=cm,scenario=scenario,archive=archive,variable=variable)
#            response = self.client.get(url)
#            self.assertTrue(response.content != None)
#            self.assertEqual(response.status_code,200)
        
        
#class OpenClimateShpTests(NetCdfAccessTest):
#    
#    def get_object(self):
#        """Return an example OpenClimateShp object."""
#        
#        qs = SpatialGridCell.objects.all().order_by('row','col')
#        geom_list = qs.values_list('geom',flat=True)
##        geom_list = obj.geom) for obj in qs]
#        na = NetCdfAccessor(self.rootgrp,self.var)
#        dl = na.get_dict(geom_list)
#        path = get_temp_path('.shp')
#        shp = OpenClimateShp(path,dl)
#        return(shp)
#    
#    def test_write(self):
#        """Write a shapefile."""
#        
#        shp = self.get_object()
#        shp.write()
        
        
#class TestHelpers(TestCase):
#    
#    def test_parse_polygon_wkt(self):
#        """Test the parsing of the polygon query string."""
#        
#        actual = 'POLYGON ((30 10,10 20,20 40,40 40,30 10))'
#        
#        qs = ['POLYGON((30+10,10+20,20+40,40+40))',
#              'polygon((30+10,10+20,20+40,40+40))',
#              'polygon((30 10,10 20,20 40,40 40))']
#        
#        for q in qs: 
#            wkt = parse_polygon_wkt(q)
#            self.assertEqual(wkt,actual)


if __name__ == '__main__':
    unittest.main()
