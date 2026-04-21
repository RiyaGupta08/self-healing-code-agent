import { motion } from 'motion/react';
import { Bot, Container, FlaskConical, Database } from 'lucide-react';

const features = [
  {
    icon: Bot,
    title: 'Autonomous Debugging',
    description: 'AI agents work independently to identify and resolve issues without human intervention',
    gradient: 'from-[#00d9ff] to-[#06b6d4]',
    stats: '99.9% accuracy',
  },
  {
    icon: Container,
    title: 'Sandbox Execution',
    description: 'Safe, isolated environments test fixes before applying them to production code',
    gradient: 'from-[#8b5cf6] to-[#a78bfa]',
    stats: 'Zero risk',
  },
  {
    icon: FlaskConical,
    title: 'Test Validation',
    description: 'Automated pytest integration ensures fixes pass all test cases and requirements',
    gradient: 'from-[#06b6d4] to-[#22d3ee]',
    stats: '100% coverage',
  },
  {
    icon: Database,
    title: 'Learning Memory',
    description: 'AI stores patterns and solutions to improve future debugging performance',
    gradient: 'from-[#a78bfa] to-[#c084fc]',
    stats: 'Always improving',
  },
];

export function FeatureCards() {
  return (
    <section className="relative px-6 py-20">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-4" style={{ fontFamily: 'Orbitron, sans-serif' }}>
            Advanced Capabilities
          </h2>
          <p className="text-lg text-[#94a3b8] max-w-2xl mx-auto" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
            Powered by cutting-edge AI technology and enterprise-grade infrastructure
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="group relative"
              >
                {/* Glassmorphic card */}
                <div className="relative h-full p-8 rounded-2xl border border-white/10 overflow-hidden backdrop-blur-md bg-gradient-to-br from-[#0f172a]/80 to-[#1e293b]/40 hover:border-white/20 transition-all duration-300">
                  {/* Gradient overlay on hover */}
                  <div
                    className={`absolute inset-0 bg-gradient-to-br ${feature.gradient} opacity-0 group-hover:opacity-5 transition-opacity duration-300`}
                  />

                  {/* Animated border glow */}
                  <div
                    className={`absolute inset-0 rounded-2xl bg-gradient-to-br ${feature.gradient} opacity-0 group-hover:opacity-20 blur-xl transition-opacity duration-300`}
                  />

                  {/* Content */}
                  <div className="relative z-10">
                    {/* Icon container */}
                    <div className="relative mb-6">
                      <div
                        className={`w-16 h-16 rounded-xl bg-gradient-to-br ${feature.gradient} p-0.5`}
                      >
                        <div className="w-full h-full rounded-xl bg-[#0a0e1a] flex items-center justify-center">
                          <Icon className="w-8 h-8 text-white" />
                        </div>
                      </div>

                      {/* Floating stat badge */}
                      <motion.div
                        initial={{ opacity: 0, x: -10 }}
                        whileInView={{ opacity: 1, x: 0 }}
                        viewport={{ once: true }}
                        transition={{ duration: 0.5, delay: index * 0.1 + 0.2 }}
                        className={`absolute -top-2 -right-2 px-3 py-1 rounded-full bg-gradient-to-r ${feature.gradient} text-xs font-semibold text-white`}
                        style={{ fontFamily: 'Space Grotesk, sans-serif' }}
                      >
                        {feature.stats}
                      </motion.div>
                    </div>

                    <h3 className="text-2xl font-bold text-white mb-3" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                      {feature.title}
                    </h3>

                    <p className="text-[#94a3b8] leading-relaxed" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                      {feature.description}
                    </p>

                    {/* Animated progress bar */}
                    <motion.div
                      initial={{ width: 0 }}
                      whileInView={{ width: '100%' }}
                      viewport={{ once: true }}
                      transition={{ duration: 1, delay: index * 0.1 + 0.3 }}
                      className="mt-6 h-1 rounded-full overflow-hidden bg-white/5"
                    >
                      <div className={`h-full bg-gradient-to-r ${feature.gradient}`} />
                    </motion.div>
                  </div>

                  {/* Corner accents */}
                  <div className={`absolute top-0 right-0 w-20 h-20 bg-gradient-to-br ${feature.gradient} opacity-10 blur-2xl rounded-full`} />
                  <div className={`absolute bottom-0 left-0 w-20 h-20 bg-gradient-to-br ${feature.gradient} opacity-10 blur-2xl rounded-full`} />
                </div>
              </motion.div>
            );
          })}
        </div>

        {/* Additional info banner */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.5 }}
          className="mt-12 p-6 rounded-2xl border border-[#00d9ff]/20 bg-gradient-to-r from-[#00d9ff]/5 via-[#8b5cf6]/5 to-[#00d9ff]/5 backdrop-blur-sm"
        >
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div>
              <h4 className="text-lg font-semibold text-white mb-1" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                Enterprise Ready
              </h4>
              <p className="text-sm text-[#94a3b8]" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                Built for scale with SOC 2 compliance, 99.9% uptime SLA, and dedicated support
              </p>
            </div>
            <button className="px-6 py-3 border border-[#00d9ff]/30 rounded-lg text-[#00d9ff] font-semibold hover:bg-[#00d9ff]/10 transition-colors whitespace-nowrap" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
              Contact Sales
            </button>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
