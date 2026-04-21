import { motion } from 'motion/react';

export function AnimatedBackground() {
  return (
    <div className="fixed inset-0 -z-10 overflow-hidden pointer-events-none">
      {/* Deep layered background */}
      <div className="absolute inset-0 bg-gradient-to-b from-[#0a0e1a] via-[#0f172a] to-[#0a0e1a]" />
      
      {/* Animated grid pattern - more prominent */}
      <div 
        className="absolute inset-0 opacity-30"
        style={{
          backgroundImage: `
            linear-gradient(rgba(0, 217, 255, 0.15) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 217, 255, 0.15) 1px, transparent 1px)
          `,
          backgroundSize: '60px 60px',
          backgroundPosition: '0 0, 0 0',
        }}
      >
        <div
          className="absolute inset-0"
          style={{
            backgroundImage: `
              linear-gradient(rgba(139, 92, 246, 0.1) 1px, transparent 1px),
              linear-gradient(90deg, rgba(139, 92, 246, 0.1) 1px, transparent 1px)
            `,
            backgroundSize: '60px 60px',
            backgroundPosition: '30px 30px, 30px 30px',
          }}
        />
      </div>
      
      {/* Noise texture - more visible */}
      <div 
        className="absolute inset-0 opacity-10"
        style={{
          backgroundImage: 'url("data:image/svg+xml,%3Csvg viewBox=\'0 0 400 400\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cfilter id=\'noiseFilter\'%3E%3CfeTurbulence type=\'fractalNoise\' baseFrequency=\'1.2\' numOctaves=\'4\' stitchTiles=\'stitch\'/%3E%3C/filter%3E%3Crect width=\'100%25\' height=\'100%25\' filter=\'url(%23noiseFilter)\'/%3E%3C/svg%3E")',
        }}
      />
      
      {/* Large radial gradients - more dramatic */}
      <motion.div 
        className="absolute -top-40 -left-40 w-[600px] h-[600px] rounded-full blur-[140px] opacity-25"
        style={{
          background: 'radial-gradient(circle, #00d9ff 0%, transparent 70%)',
        }}
        animate={{
          scale: [1, 1.2, 1],
          opacity: [0.25, 0.35, 0.25],
        }}
        transition={{
          duration: 8,
          repeat: Infinity,
          ease: 'easeInOut',
        }}
      />
      
      <motion.div 
        className="absolute top-1/3 right-0 w-[600px] h-[600px] rounded-full blur-[140px] opacity-20"
        style={{
          background: 'radial-gradient(circle, #8b5cf6 0%, transparent 70%)',
        }}
        animate={{
          scale: [1, 1.3, 1],
          opacity: [0.2, 0.3, 0.2],
        }}
        transition={{
          duration: 10,
          repeat: Infinity,
          ease: 'easeInOut',
          delay: 1,
        }}
      />

      <motion.div 
        className="absolute bottom-0 left-1/3 w-[500px] h-[500px] rounded-full blur-[120px] opacity-20"
        style={{
          background: 'radial-gradient(circle, #06b6d4 0%, transparent 70%)',
        }}
        animate={{
          scale: [1, 1.15, 1],
          opacity: [0.2, 0.28, 0.2],
        }}
        transition={{
          duration: 9,
          repeat: Infinity,
          ease: 'easeInOut',
          delay: 2,
        }}
      />
      
      {/* Animated energy lines */}
      <svg className="absolute inset-0 w-full h-full opacity-40">
        <defs>
          <linearGradient id="lineGradient1" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#00d9ff" stopOpacity="0" />
            <stop offset="50%" stopColor="#00d9ff" stopOpacity="0.8" />
            <stop offset="100%" stopColor="#00d9ff" stopOpacity="0" />
          </linearGradient>
          <linearGradient id="lineGradient2" x1="100%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="#8b5cf6" stopOpacity="0" />
            <stop offset="50%" stopColor="#8b5cf6" stopOpacity="0.8" />
            <stop offset="100%" stopColor="#8b5cf6" stopOpacity="0" />
          </linearGradient>
        </defs>
        
        <line x1="0" y1="15%" x2="100%" y2="15%" stroke="url(#lineGradient1)" strokeWidth="2">
          <animate attributeName="y1" values="15%;85%;15%" dur="25s" repeatCount="indefinite" />
          <animate attributeName="y2" values="15%;85%;15%" dur="25s" repeatCount="indefinite" />
          <animate attributeName="opacity" values="0.3;0.6;0.3" dur="25s" repeatCount="indefinite" />
        </line>
        
        <line x1="0" y1="60%" x2="100%" y2="60%" stroke="url(#lineGradient2)" strokeWidth="2">
          <animate attributeName="y1" values="60%;25%;60%" dur="30s" repeatCount="indefinite" />
          <animate attributeName="y2" values="60%;25%;60%" dur="30s" repeatCount="indefinite" />
          <animate attributeName="opacity" values="0.3;0.5;0.3" dur="30s" repeatCount="indefinite" />
        </line>

        <line x1="20%" y1="0" x2="20%" y2="100%" stroke="url(#lineGradient1)" strokeWidth="1.5">
          <animate attributeName="x1" values="20%;80%;20%" dur="35s" repeatCount="indefinite" />
          <animate attributeName="x2" values="20%;80%;20%" dur="35s" repeatCount="indefinite" />
          <animate attributeName="opacity" values="0.2;0.5;0.2" dur="35s" repeatCount="indefinite" />
        </line>
      </svg>

      {/* Vignette overlay */}
      <div 
        className="absolute inset-0"
        style={{
          background: 'radial-gradient(circle at center, transparent 0%, rgba(10, 14, 26, 0.8) 100%)',
        }}
      />
    </div>
  );
}
