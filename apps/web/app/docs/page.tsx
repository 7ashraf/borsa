import { Navbar } from "@/components/navbar";
import { Footer } from "@/components/footer";
import { DocsContent } from "@/components/docs-content";

export const metadata = {
  title: "Docs — borsa",
  description: "borsa API documentation: endpoints, examples, self-hosting guide.",
};

export default function DocsPage() {
  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      <main className="flex-1 pt-14">
        <DocsContent />
      </main>
      <Footer />
    </div>
  );
}
