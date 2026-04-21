import { Github, Twitter, Linkedin, Mail, Code2 } from 'lucide-react';

export function Footer() {
  return (
    <footer className="relative border-t border-[#00d9ff]/10 bg-[#0a0e1a]/50 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-6 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-12 mb-12">
          {/* Brand */}
          <div className="md:col-span-2">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-[#00d9ff] to-[#06b6d4] flex items-center justify-center">
                <Code2 className="w-6 h-6 text-[#0a0e1a]" />
              </div>
              <span className="text-xl font-bold text-white" style={{ fontFamily: 'Orbitron, sans-serif' }}>
                Self-Healing Code
              </span>
            </div>
            <p className="text-[#94a3b8] mb-6 max-w-sm" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
              Autonomous AI-powered debugging that fixes your code while you focus on building great products.
            </p>
            <div className="flex gap-4">
              {[
                { icon: Github, href: '#' },
                { icon: Twitter, href: '#' },
                { icon: Linkedin, href: '#' },
                { icon: Mail, href: '#' },
              ].map((social, index) => {
                const Icon = social.icon;
                return (
                  <a
                    key={index}
                    href={social.href}
                    className="w-10 h-10 rounded-lg border border-[#00d9ff]/20 bg-[#00d9ff]/5 flex items-center justify-center text-[#94a3b8] hover:text-[#00d9ff] hover:border-[#00d9ff]/40 hover:bg-[#00d9ff]/10 transition-all duration-300"
                  >
                    <Icon className="w-5 h-5" />
                  </a>
                );
              })}
            </div>
          </div>

          {/* Product */}
          <div>
            <h4 className="font-semibold text-white mb-4" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
              Product
            </h4>
            <ul className="space-y-3">
              {['Features', 'Pricing', 'Use Cases', 'Documentation'].map((item) => (
                <li key={item}>
                  <a
                    href="#"
                    className="text-[#94a3b8] hover:text-[#00d9ff] transition-colors"
                    style={{ fontFamily: 'Space Grotesk, sans-serif' }}
                  >
                    {item}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Company */}
          <div>
            <h4 className="font-semibold text-white mb-4" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
              Company
            </h4>
            <ul className="space-y-3">
              {['About', 'Blog', 'Careers', 'Contact'].map((item) => (
                <li key={item}>
                  <a
                    href="#"
                    className="text-[#94a3b8] hover:text-[#00d9ff] transition-colors"
                    style={{ fontFamily: 'Space Grotesk, sans-serif' }}
                  >
                    {item}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Bottom bar */}
        <div className="pt-8 border-t border-[#00d9ff]/10 flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-sm text-[#64748b]" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
            © 2026 Self-Healing Code. All rights reserved.
          </p>
          <div className="flex gap-6">
            {['Privacy', 'Terms', 'Security'].map((item) => (
              <a
                key={item}
                href="#"
                className="text-sm text-[#64748b] hover:text-[#00d9ff] transition-colors"
                style={{ fontFamily: 'Space Grotesk, sans-serif' }}
              >
                {item}
              </a>
            ))}
          </div>
        </div>
      </div>

      {/* Background glow */}
      <div className="absolute bottom-0 left-1/4 w-96 h-96 bg-[#00d9ff] rounded-full blur-[150px] opacity-5 pointer-events-none" />
    </footer>
  );
}
