// Project world_geo.json and transport_curated.csv points to a 960x470 Equal Earth SVG frame.
// Usage (needs npm packages d3-geo@3.1.1): node project_geo.mjs maps/world_geo.json maps/transport_curated.csv maps/world_svg.json maps/transport_xy.json
import fs from 'fs';
import {geoEqualEarth, geoPath} from 'd3-geo';
const [,,geoIn,transIn,outGeo,outPts]=process.argv;
const rows=JSON.parse(fs.readFileSync(geoIn));
const fc={type:'FeatureCollection',features:rows.map(r=>({type:'Feature',properties:{iso3:r.iso3,name:r.name},geometry:JSON.parse(r.geometry)}))};
const W=960,H=470;
const proj=geoEqualEarth().fitExtent([[4,4],[W-4,H-4]],fc);
const path=geoPath(proj).digits(1);
const out=fc.features.map(f=>{const c=path.centroid(f);return {iso3:f.properties.iso3,name:f.properties.name,path:path(f)||'',cx:+c[0].toFixed(1),cy:+c[1].toFixed(1)}});
// better centroid for multi-part countries: use largest polygon
for(const o of out){const f=fc.features.find(x=>x.properties.iso3===o.iso3&&x.properties.name===o.name);
 if(f.geometry.type==='MultiPolygon'){let best=null,ba=-1;for(const p of f.geometry.coordinates){const g={type:'Polygon',coordinates:p};const a=path.area(g);if(a>ba){ba=a;best=g}}const c=path.centroid(best);o.cx=+c[0].toFixed(1);o.cy=+c[1].toFixed(1);}}
fs.writeFileSync(outGeo,JSON.stringify(out));
const lines=fs.readFileSync(transIn,'utf8').trim().split('\n');
console.log(out.length,fs.statSync(outGeo).size);

const hdr=lines[0].split(',');const li=hdr.indexOf('lat'),lo=hdr.indexOf('lon');
const pts=[];for(const l of lines.slice(1)){const c=l.split(',');if(c[li]&&c[lo]){const p=proj([+c[lo],+c[li]]);pts.push({place:c[1],x:+p[0].toFixed(1),y:+p[1].toFixed(1)});}}
fs.writeFileSync(outPts,JSON.stringify(pts));console.log(pts.length);
