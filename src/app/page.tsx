
import MapWGS84 from "@/components/MapWGS84";
// import { buildWindLayer } from "@/components/MapFetcher";


export default async function Home() {
  // const windLayer = await buildWindLayer();

  return (
    <MapWGS84 /> 
  );
}
