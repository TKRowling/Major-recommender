import React from "react";
import "../styles/app.css";

function TestimonialSection() {
  return (
    <section className="testimonial-section">
      <div className="testimonial-container">
        <p className="testimonial-quote">
          “Choose a major that builds your future,
          not just one that fills your schedule.”
        </p>

        <div className="testimonial-author">
          <h4>AN Hengheng</h4>
          <span>Student '20</span>
        </div>
      </div>
    </section>
  );
}

export default TestimonialSection;