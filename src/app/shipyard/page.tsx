import InputLabel from "@/components/InputLabel";

export default async function Home() {
  // const windLayer = await buildWindLayer();

  const formId: string = "boat-form";

  return (
    <div className="grid grid-rows-[20px_1fr_10px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <h1>Winged Watch</h1>
      <form id={formId} className="grid grid-cols-1 gap-4">
        <InputLabel form={formId} type ="text" id="boat-name" placeholder="Boat name" />
        <InputLabel form={formId} type ="number" id="boat-draught" placeholder="Boat draught" />
        <InputLabel form={formId} type ="number" id="boat-sails" placeholder="Boat sails (square meters)" />
      </form>  
    </div>
  );
}