import MapWGS84 from "@/components/MapWGS84";
// import { buildWindLayer } from "@/components/MapFetcher";


export default async function Home() {
  // const windLayer = await buildWindLayer();

  return (
    <div className="grid grid-rows-[20px_1fr_10px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <h1>Winged Watch</h1>
      <MapWGS84 /> 
    </div>
  );
}
