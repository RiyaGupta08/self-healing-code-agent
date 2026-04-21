import { AnimatedBackground } from './components/AnimatedBackground';
import { ParticleField } from './components/ParticleField';
import { ProfessionalNav } from './components/ProfessionalNav';
import { FigmaHeroSection } from './components/FigmaHeroSection';
import { CodeInterface } from './components/CodeInterface';
import { ProcessFlow } from './components/ProcessFlow';
import { FeatureCards } from './components/FeatureCards';
import { Footer } from './components/Footer';

export default function App() {
  return (
    <div className="min-h-screen bg-[#0a0e1a] text-white relative overflow-hidden">
      <ProfessionalNav />

      {/* Main content */}
      <main>
        <FigmaHeroSection />
        <CodeInterface />
        <ProcessFlow />
        <FeatureCards />
      </main>

      <Footer />
    </div>
  );
}