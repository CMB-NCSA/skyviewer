var a1 = A.aladin('#al1',
  {
    cooFrame: 'equatorial',
    projection: "ZEA",
    fov: 90,
    realFullscreen: true,
    target: '0 0 0 -56 45 0',
    survey: 'P/DES-DR2/ColorIRG'
  }
);
a1.createImageSurvey("P/DES-DR2/ColorIRG", "DES-DR2 ColorIRG", "https://alasky.cds.unistra.fr/DES/DR2/CDS_P_DES-DR2_ColorIRG", "equatorial", 11, {imgFormat: "png"});
a1.setBaseImageLayer("P/DES-DR2/ColorIRG",{imgFormat: "png"});
a1.setFovRange(0.01, 175);

var hipsDir090 = `./hips/SPT_winter2020_090GHz_HiPS/`;
hipsDir090 = hipsDir090.substring(0,hipsDir090.lastIndexOf("/",hipsDir090.length));
var hipsDir150 = `./hips/SPT_winter2020_150GHz_HiPS/`;
hipsDir150 = hipsDir150.substring(0,hipsDir150.lastIndexOf("/",hipsDir150.length));
var hipsDir220 = `./hips/SPT_winter2020_220GHz_HiPS/`;
hipsDir220 = hipsDir220.substring(0,hipsDir220.lastIndexOf("/",hipsDir220.length));

var a2 = A.aladin('#al2',
  {
   cooFrame: 'equatorial',
   projection: "ZEA",
   fov: 90,
   realFullscreen: true,
   target: '0 0 0 -56 45 0',
   showFrameControl: false, showFullscreenControl: false, showGotoControl: false,
 }
);

a2.createImageSurvey('SPT_winter2020_090GHz0_HiPS', 'SPT Winter2020 090GHz', hipsDir090, 'equatorial', 5, {imgFormat: 'png'});
a2.createImageSurvey('SPT_winter2020_150GHz0_HiPS', 'SPT Winter2020 150GHz', hipsDir150, 'equatorial', 5, {imgFormat: 'png'});
a2.createImageSurvey('SPT_winter2020_220GHz0_HiPS', 'SPT Winter2020 200GHz', hipsDir220, 'equatorial', 5, {imgFormat: 'png'});
a2.setBaseImageLayer("SPT_winter2020_150GHz0_HiPS",{imgFormat: "png"});
a2.getBaseImageLayer().getColorMap().update('rainbow')

View.CALLBACKS_THROTTLE_TIME = 30;
a1.on('positionChanged', function(params) {
    a2.gotoRaDec(params.ra, params.dec);
});
a2.on('positionChanged', function(params) {
    a1.gotoRaDec(params.ra, params.dec);
});
a1.on('zoomChanged', function(fov) {
if (Math.abs(a2.getFov()[0] - fov) / fov > 0.01) {
        a2.setFoV(fov);
    }
});
a2.on('zoomChanged', function(fov) {
    if (Math.abs(a1.getFov()[0] - fov) / fov > 0.01) {
        a1.setFoV(fov);
    }
});
setTimeout(function() {
    $(".twentytwenty-container").twentytwenty({default_offset_pct: 0.5, no_overlay: true});
}, 300);
