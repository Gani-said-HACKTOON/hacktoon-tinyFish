"use client";

import { useState } from "react";

export default function ContactUs() {
  const [submitted, setSubmitted] = useState(false);

const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setSubmitted(true);
};

  return (
    <section className="min-h-screen flex items-center justify-center px-4 py-20">
      <div className="w-full max-w-lg">

        {/* Badge */}
        <div className="flex justify-center mb-6">
          <span className="text-xs font-semibold tracking-widest uppercase bg-gray-100 text-gray-500 rounded-full px-4 py-1.5 border border-gray-200">
            Contact Us
          </span>
        </div>

        {/* Heading */}
        <h1 className="text-4xl md:text-5xl font-bold text-center text-gray-900 mb-3 leading-tight">
          Let's connect
        </h1>
        <p className="text-center text-gray-500 text-base md:text-lg mb-10 max-w-sm mx-auto">
          Have questions? Contact us and we'll be happy to help.
        </p>

        {/* Card */}
        <div className="bg-white rounded-3xl shadow-xl border border-gray-100 p-8 md:p-10">
          {submitted ? (
            <div className="flex flex-col items-center justify-center py-10 gap-4">
              <div className="w-16 h-16 rounded-full bg-black flex items-center justify-center">
                <svg className="w-8 h-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <h2 className="text-xl font-bold text-gray-900">Message Sent!</h2>
              <p className="text-gray-500 text-center text-sm">We'll get back to you as soon as possible.</p>
              <button
                onClick={() => setSubmitted(false)}
                className="mt-2 text-sm font-semibold text-gray-500 underline underline-offset-4 hover:text-gray-800 transition-colors"
              >
                Send another message
              </button>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="flex flex-col gap-5">

              {/* Name */}
              <div className="flex flex-col gap-1.5">
                <label className="text-sm font-semibold text-gray-700">Name</label>
                <input
                  type="text"
                  placeholder="Eg. Jane Smith"
                  required
                  className="w-full rounded-xl border border-gray-200 bg-gray-50 px-4 py-3 text-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent transition"
                />
              </div>

              {/* Email */}
              <div className="flex flex-col gap-1.5">
                <label className="text-sm font-semibold text-gray-700">Email</label>
                <input
                  type="email"
                  placeholder="jane@framer.com"
                  required
                  className="w-full rounded-xl border border-gray-200 bg-gray-50 px-4 py-3 text-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent transition"
                />
              </div>

              {/* Message */}
              <div className="flex flex-col gap-1.5">
                <label className="text-sm font-semibold text-gray-700">Message</label>
                <textarea
                  placeholder="Enter your message..."
                  required
                  rows={4}
                  className="w-full rounded-xl border border-gray-200 bg-gray-50 px-4 py-3 text-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent transition resize-none"
                />
              </div>

              {/* Existing Customer */}
              <div className="flex flex-col gap-1.5">
                <label className="text-sm font-semibold text-gray-700">Are you an existing customer?</label>
                <div className="relative">
                  <select
                    required
                    defaultValue=""
                    className="w-full appearance-none rounded-xl border border-gray-200 bg-gray-50 px-4 py-3 text-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent transition cursor-pointer"
                  >
                    <option value="" disabled>Select...</option>
                    <option value="yes">Yes</option>
                    <option value="no">No</option>
                  </select>
                  <div className="pointer-events-none absolute inset-y-0 right-4 flex items-center">
                    <svg className="w-4 h-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
                    </svg>
                  </div>
                </div>
              </div>

              {/* Submit */}
              <button
                type="submit"
                className="w-full mt-2 bg-gray-900 hover:bg-gray-700 active:scale-95 text-white font-semibold rounded-xl py-3.5 text-sm transition-all duration-150"
              >
                Send a message
              </button>

            </form>
          )}
        </div>

      </div>
    </section>
  );
}