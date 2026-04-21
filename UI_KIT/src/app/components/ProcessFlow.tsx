import { motion } from 'motion/react';
import { Eye, Brain, MapPin, Zap, CheckCircle, BookOpen, ArrowRight } from 'lucide-react';

const steps = [
  {
    icon: Eye,
    title: 'Observe',
    description: 'Detects errors and analyzes code behavior',
    color: '#00d9ff',
  },
  {
    icon: Brain,
    title: 'Reason',
    description: 'Understands root cause and context',
    color: '#8b5cf6',
  },
  {
    icon: MapPin,
    title: 'Plan',
    description: 'Designs optimal fix strategy',
    color: '#06b6d4',
  },
  {
    icon: Zap,
    title: 'Act',
    description: 'Implements and applies the fix',
    color: '#a78bfa',
  },
  {
    icon: CheckCircle,
    title: 'Verify',
    description: 'Validates fix with automated tests',
    color: '#22c55e',
  },
  {
    icon: BookOpen,
    title: 'Learn',
    description: 'Stores knowledge for future improvements',
    color: '#eab308',
  },
];

export function ProcessFlow() {
  return (
    <section className="relative px-6 py-32 overflow-hidden">
      {/* Background accent */}
      <div className="absolute top-1/2 left-0 w-96 h-96 bg-[#8b5cf6]/20 rounded-full blur-[150px]" />
      
      <div className="max-w-7xl mx-auto">
        {/* Section header - asymmetric */}
        <div className="mb-20 relative max-w-4xl">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <div className="flex items-center gap-3 mb-4">
              <div className="flex gap-1">
                <div className="w-2 h-2 rounded-full bg-[#00d9ff]" />
                <div className="w-2 h-2 rounded-full bg-[#8b5cf6]" />
                <div className="w-2 h-2 rounded-full bg-[#06b6d4]" />
              </div>
              <span className="text-sm text-[#00d9ff] uppercase tracking-wider font-semibold" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                How It Works
              </span>
            </div>
            <h2 className="text-5xl md:text-7xl font-black text-white mb-6 tracking-tight" style={{ fontFamily: 'Orbitron, sans-serif' }}>
              AGENTIC
              <br />
              <span className="bg-gradient-to-r from-[#00d9ff] to-[#8b5cf6] bg-clip-text text-transparent">
                PROCESS LOOP
              </span>
            </h2>
            <p className="text-xl text-[#94a3b8]" style={{ fontFamily: 'Space Grotesk, sans-serif', fontWeight: 300 }}>
              Our AI follows a sophisticated autonomous loop to fix your code
            </p>
          </motion.div>
        </div>

        <div className="relative">
          {/* Flowing connection line - desktop */}
          <svg className="hidden lg:block absolute top-24 left-0 w-full h-full pointer-events-none" style={{ zIndex: 0 }}>
            <defs>
              <linearGradient id="flowGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stopColor="#00d9ff" stopOpacity="0.6" />
                <stop offset="50%" stopColor="#8b5cf6" stopOpacity="0.6" />
                <stop offset="100%" stopColor="#00d9ff" stopOpacity="0.6" />
              </linearGradient>
            </defs>
            <motion.path
              d="M 100 50 Q 300 50, 400 50 T 700 50 T 1000 50 T 1300 50"
              stroke="url(#flowGradient)"
              strokeWidth="3"
              fill="none"
              strokeDasharray="10 5"
              initial={{ pathLength: 0, opacity: 0 }}
              whileInView={{ pathLength: 1, opacity: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 2, ease: 'easeInOut' }}
            />
          </svg>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 lg:gap-6 relative" style={{ zIndex: 1 }}>
            {steps.map((step, index) => {
              const Icon = step.icon;
              return (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 40, scale: 0.9 }}
                  whileInView={{ opacity: 1, y: 0, scale: 1 }}
                  viewport={{ once: true }}
                  transition={{ 
                    duration: 0.6, 
                    delay: index * 0.15,
                    type: 'spring',
                    stiffness: 100,
                  }}
                  className="relative"
                >
                  <div className="group relative h-full p-8 rounded-2xl border backdrop-blur-xl hover:scale-105 transition-all duration-500"
                    style={{
                      borderColor: `${step.color}40`,
                      background: `linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.7) 100%)`,
                    }}
                  >
                    {/* Intense glow effect on hover */}
                    <div
                      className="absolute -inset-1 rounded-2xl opacity-0 group-hover:opacity-100 blur-2xl transition-all duration-500"
                      style={{
                        background: `radial-gradient(circle at center, ${step.color}60, transparent 70%)`,
                      }}
                    />

                    {/* Step number with unique design */}
                    <div className="absolute -top-5 -right-5 w-14 h-14 rounded-2xl border-2 bg-[#0a0e1a] flex items-center justify-center font-black text-lg shadow-2xl rotate-12 group-hover:rotate-0 transition-transform duration-500"
                      style={{
                        borderColor: step.color,
                        color: step.color,
                        boxShadow: `0 0 30px ${step.color}40`,
                      }}
                    >
                      {index + 1}
                    </div>

                    {/* Content */}
                    <div className="relative">
                      <div
                        className="w-16 h-16 rounded-2xl flex items-center justify-center mb-6 relative overflow-hidden group-hover:scale-110 transition-transform duration-500"
                        style={{
                          background: `linear-gradient(135deg, ${step.color}30, ${step.color}10)`,
                          border: `2px solid ${step.color}50`,
                          boxShadow: `0 0 20px ${step.color}30`,
                        }}
                      >
                        <Icon className="w-8 h-8 relative z-10" style={{ color: step.color }} />
                        
                        {/* Icon glow */}
                        <motion.div
                          className="absolute inset-0"
                          animate={{
                            opacity: [0.3, 0.6, 0.3],
                          }}
                          transition={{
                            duration: 2,
                            repeat: Infinity,
                            delay: index * 0.3,
                          }}
                          style={{
                            background: `radial-gradient(circle, ${step.color}60, transparent)`,
                          }}
                        />
                      </div>

                      <h3 className="text-2xl font-black text-white mb-3 tracking-tight" style={{ fontFamily: 'Orbitron, sans-serif' }}>
                        {step.title}
                      </h3>

                      <p className="text-sm text-[#94a3b8] leading-relaxed" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                        {step.description}
                      </p>
                    </div>

                    {/* Animated pulse indicator */}
                    <motion.div
                      className="absolute bottom-6 right-6 w-3 h-3 rounded-full"
                      style={{ backgroundColor: step.color }}
                      animate={{
                        scale: [1, 1.5, 1],
                        opacity: [0.5, 1, 0.5],
                      }}
                      transition={{
                        duration: 2,
                        repeat: Infinity,
                        delay: index * 0.3,
                      }}
                    />

                    {/* Corner accents */}
                    <div className="absolute top-0 left-0 w-6 h-6 border-t-2 border-l-2 rounded-tl-2xl" style={{ borderColor: step.color, opacity: 0.3 }} />
                    <div className="absolute bottom-0 right-0 w-6 h-6 border-b-2 border-r-2 rounded-br-2xl" style={{ borderColor: step.color, opacity: 0.3 }} />
                  </div>

                  {/* Arrow connector for mobile/tablet */}
                  {index < steps.length - 1 && (
                    <div className="lg:hidden flex justify-center my-6">
                      <motion.div
                        initial={{ opacity: 0, y: -10 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ delay: index * 0.1 + 0.3 }}
                        className="flex flex-col items-center gap-2"
                      >
                        <div className="w-px h-8 bg-gradient-to-b from-[#00d9ff]/50 to-[#8b5cf6]/50" />
                        <ArrowRight className="w-5 h-5 text-[#00d9ff] rotate-90" />
                      </motion.div>
                    </div>
                  )}
                </motion.div>
              );
            })}
          </div>

          {/* Enhanced circular flow indicator */}
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 1 }}
            className="mt-16 relative"
          >
            <div className="flex items-center justify-center gap-4 p-6 rounded-2xl border border-[#00d9ff]/30 bg-gradient-to-r from-[#0f172a]/90 to-[#1e293b]/70 backdrop-blur-xl w-fit mx-auto relative overflow-hidden group">
              {/* Glow effect */}
              <div className="absolute inset-0 bg-gradient-to-r from-[#00d9ff]/10 via-[#8b5cf6]/10 to-[#00d9ff]/10 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
              
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 4, repeat: Infinity, ease: 'linear' }}
                className="relative"
              >
                <div className="w-12 h-12 rounded-full bg-gradient-to-br from-[#00d9ff] to-[#8b5cf6] flex items-center justify-center">
                  <BookOpen className="w-6 h-6 text-white" />
                </div>
                <div className="absolute inset-0 rounded-full bg-gradient-to-br from-[#00d9ff] to-[#8b5cf6] blur-lg opacity-50" />
              </motion.div>
              
              <div className="relative">
                <span className="text-lg font-bold text-white block" style={{ fontFamily: 'Orbitron, sans-serif' }}>
                  CONTINUOUS LEARNING LOOP
                </span>
                <span className="text-sm text-[#94a3b8]" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                  Always improving, never stopping
                </span>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}