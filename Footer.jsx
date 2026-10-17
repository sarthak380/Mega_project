import React from 'react';

function Footer() {
  return (
    <footer className="footer mt-auto py-5 text-white" style={{ backgroundColor: '#002b49' }}>
      <div className="container">
        <h2 className="mb-5 fw-bold text-uppercase">Contact Us</h2>
        
        <div className="row">
          {/* Market Yard Section */}
          <div className="col-md-6 mb-4">
            <h5 className="fw-bold mb-3">📍 SUNBEAM MARKET YARD PUNE</h5>
            <p className="text-light opacity-75">
              'Sunbeam Chambers', Plot No.R/2, Market Yard Road, Behind Hotel Fulora, Gultekdi,<br />
              Pune - 411 037. MH-INDIA.
            </p>
            <div className="mt-4">
              {/* Mobile Number with Sign */}
              <p className="mb-2">
                <span style={{ fontSize: '1.2rem' }}>📱</span> <strong>+91 82 82 82 9806</strong>
              </p>
              {/* Email with Sign */}
              <p>
                <span style={{ fontSize: '1.2rem' }}>✉️</span> <strong> scc@sunbeaminfo.in</strong>
              </p>
            </div>
          </div>

          {/* Hinjawadi Section */}
          <div className="col-md-6 mb-4">
            <h5 className="fw-bold mb-3">📍 SUNBEAM HINJAWADI PUNE</h5>
            <p className="text-light opacity-75">
              "Sunbeam IT Park", Second Floor, Phase 2 of Rajiv Gandhi Infotech Park, Hinjawadi,<br />
              Pune - 411057, MH-INDIA
            </p>
            <div className="mt-4">
              <p className="mb-2">
                <span style={{ fontSize: '1.2rem' }}>📱</span> <strong>+91 82 82 82 9806</strong>
              </p>
              <p>
                <span style={{ fontSize: '1.2rem' }}>✉️</span> <strong>scc@sunbeaminfo.in</strong>
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Strip */}
      <div className="container-fluid py-3 mt-5" style={{ backgroundColor: '#001a2c', borderTop: '1px solid rgba(255,255,255,0.1)' }}>
        <div className="container d-flex justify-content-between align-items-center small text-secondary">
          <p className="mb-0">Sunbeam. © 2025. All Rights Reserved.</p>
          <div>
            <span className="mx-2">Webmail</span> | 
            <span className="mx-2">FAQs</span> | 
            <span className="mx-2">Sitemap</span> | 
            <span className="mx-2">Privacy</span>
          </div>
          <p className="mb-0">Powered by <strong>ganesh mali</strong></p>
        </div>
      </div>
    </footer>
  );
}

export default Footer;