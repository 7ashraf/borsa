import { Navbar } from "@/components/navbar";
import { Hero } from "@/components/hero";
import { LiveDemo } from "@/components/live-demo";
import { WhySection } from "@/components/why-section";
import { HowItWorks } from "@/components/how-it-works";
import { CodeExamples } from "@/components/code-examples";
import { FeatureGrid } from "@/components/feature-grid";
import { Faq } from "@/components/faq";
import { Footer } from "@/components/footer";

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      <main className="flex-1">
        <Hero />
        <LiveDemo />
        <WhySection />
        <HowItWorks />
        <CodeExamples />
        <FeatureGrid />
        <Faq />
      </main>
      <Footer />
    </div>
  );
}
