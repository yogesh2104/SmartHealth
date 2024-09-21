import { Button } from "@/components/ui/button";
import Heading from "./_components/heading";
import Heroes from "./_components/heroes";
import FooterPage from "./_components/footer";

export default function MarketingPage() {
  return (
   <div className="min-h-full flex flex-col">
    <div className="flex flex-col items-center justify-center md:justify-start text-center gap-y-8 flex-1 px-6 pb-10 dark:bg-[#1f1f1f]">
      <Heading/>
      {/* <Heroes/> */}
    </div>
   </div>
  )
}
