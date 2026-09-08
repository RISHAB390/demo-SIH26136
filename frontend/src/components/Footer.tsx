import React from 'react';
import { Globe, Mail, Phone, ExternalLink } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="gov-footer">
      <div className="gov-footer-top">
        <div className="gov-footer-grid">
          {/* SECTION 1: Government Identity */}
          <div className="gov-footer-col gov-footer-identity-col">
            <div className="gov-footer-brand">
              <div className="gov-emblem-wrapper" title="महाराष्ट्र शासन | Government of Maharashtra">
                <svg
                  className="gov-emblem-svg"
                  viewBox="0 0 100 100"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                  aria-label="Government of Maharashtra Seal"
                >
                  <circle cx="50" cy="50" r="46" stroke="#D4AF37" strokeWidth="3" fill="#161B22" />
                  <circle cx="50" cy="50" r="41" stroke="#D4AF37" strokeWidth="1" strokeDasharray="3 3" />
                  <path
                    d="M50 18 L53 27 L62 27 L55 33 L57 42 L50 37 L43 42 L45 33 L38 27 L47 27 Z"
                    fill="#D4AF37"
                  />
                  <path
                    d="M32 48 C32 44 68 44 68 48 C68 62 50 78 50 78 C50 78 32 62 32 48 Z"
                    stroke="#D4AF37"
                    strokeWidth="2"
                    fill="none"
                  />
                  <path
                    d="M38 52 L50 68 L62 52"
                    stroke="#D4AF37"
                    strokeWidth="1.5"
                    strokeLinecap="round"
                  />
                  <circle cx="50" cy="54" r="3" fill="#D4AF37" />
                  <path d="M40 82 H60" stroke="#D4AF37" strokeWidth="2" strokeLinecap="round" />
                </svg>
              </div>
              <div className="gov-state-text">
                <span className="gov-state-mr">महाराष्ट्र शासन</span>
                <span className="gov-state-en">Government of Maharashtra</span>
              </div>
            </div>

            <p className="gov-footer-mission">
              GovTech Innovation & Pilot Lifecycle Platform
            </p>

            <div className="gov-footer-motto-row">
              <span>Digital Governance</span>
              <span className="gov-footer-dot">|</span>
              <span>Inclusive Growth</span>
              <span className="gov-footer-dot">|</span>
              <span>Viksit Maharashtra</span>
            </div>

            {/* SECTION 5: Connectivity / Contact */}
            <div className="gov-footer-connect">
              <span className="gov-footer-connect-label">Stay Connected:</span>
              <div className="gov-footer-social-icons">
                <span className="gov-social-icon-btn" title="Official Web Portal" aria-label="Official Web Portal">
                  <Globe size={14} />
                </span>
                <span className="gov-social-icon-btn" title="Contact Email" aria-label="Contact Email">
                  <Mail size={14} />
                </span>
                <span className="gov-social-icon-btn" title="Toll-Free Helpline" aria-label="Toll-Free Helpline">
                  <Phone size={14} />
                </span>
              </div>
            </div>
          </div>

          {/* SECTION 2: Quick Links */}
          <div className="gov-footer-col">
            <h4 className="gov-footer-heading">Quick Links</h4>
            <ul className="gov-footer-list">
              <li><span className="gov-footer-link">Home</span></li>
              <li><span className="gov-footer-link">About Us</span></li>
              <li><span className="gov-footer-link">Contact Us</span></li>
              <li><span className="gov-footer-link">Help & Support</span></li>
            </ul>
          </div>

          {/* SECTION 3: Resources */}
          <div className="gov-footer-col">
            <h4 className="gov-footer-heading">Resources</h4>
            <ul className="gov-footer-list">
              <li><span className="gov-footer-link">User Manual</span></li>
              <li><span className="gov-footer-link">FAQs</span></li>
              <li><span className="gov-footer-link">Terms & Conditions</span></li>
              <li><span className="gov-footer-link">Privacy Policy</span></li>
            </ul>
          </div>

          {/* SECTION 4: Related Portals */}
          <div className="gov-footer-col">
            <h4 className="gov-footer-heading">Related Portals</h4>
            <ul className="gov-footer-list">
              <li>
                <span className="gov-footer-link gov-footer-external-link">
                  Maharashtra State Portal <ExternalLink size={11} />
                </span>
              </li>
              <li>
                <span className="gov-footer-link gov-footer-external-link">
                  GeM (Government e-Marketplace) <ExternalLink size={11} />
                </span>
              </li>
              <li>
                <span className="gov-footer-link gov-footer-external-link">
                  Startup Maharashtra <ExternalLink size={11} />
                </span>
              </li>
              <li>
                <span className="gov-footer-link gov-footer-external-link">
                  Digital India <ExternalLink size={11} />
                </span>
              </li>
            </ul>
          </div>
        </div>
      </div>

      {/* Bottom Copyright & Compliance Bar */}
      <div className="gov-footer-bottom">
        <div className="gov-footer-bottom-inner">
          <p className="gov-copyright-text">
            © 2026 Government of Maharashtra. All rights reserved.
          </p>
          <p className="gov-footer-disclaimer">
            GovTech Innovation & Pilot Lifecycle Platform &bull; Department of Information Technology & Municipal Administration
          </p>
        </div>
      </div>
    </footer>
  );
};
