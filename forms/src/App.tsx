import { useState } from 'react';

// --- Types ---
interface FormData {
  name: string;
  phone: string;
  email: string;
  type: string;
  message: string;
}

interface FormErrors {
  name?: string;
  phone?: string;
  email?: string;
  type?: string;
  message?: string;
}

// --- Validation ---
function validate(data: FormData): FormErrors {
  const errors: FormErrors = {};

  if (!data.name.trim()) {
    errors.name = 'Name is required.';
  }

  if (!data.phone.trim()) {
    errors.phone = 'Phone number is required.';
  } else if (!/^\d{10,15}$/.test(data.phone.trim())) {
    errors.phone = 'Enter a valid numeric phone number (10–15 digits).';
  }

  if (!data.email.trim()) {
    errors.email = 'Email is required.';
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email.trim())) {
    errors.email = 'Enter a valid email address.';
  }

  if (!data.type) {
    errors.type = 'Please select an inquiry type.';
  }

  if (!data.message.trim()) {
    errors.message = 'Message is required.';
  }

  return errors;
}

// --- Common Field Wrapper ---
const FieldWrapper = ({ id, label, error, children }: any) => (
  <div className="flex flex-col gap-1.5 w-full">
    <label htmlFor={id} className="text-sm font-bold text-slate-700">
      {label} <span className="text-rose-500">*</span>
    </label>
    {children}
    {error && (
      <p className="text-xs text-rose-500 font-bold flex items-center gap-1 mt-0.5">
        <span>⚠</span> {error}
      </p>
    )}
  </div>
);

// --- InputField Component ---
const inputClass = (error: boolean) => 
  `w-full px-4 py-3 rounded-lg border text-base text-slate-800 placeholder-slate-400 bg-white transition-all duration-200 outline-none focus:ring-2 focus:ring-vit-red/30 focus:border-vit-red ${error ? 'border-rose-400 bg-rose-50/50' : 'border-slate-200 hover:border-slate-300'}`;

function InputField({ id, label, type = 'text', value, error, placeholder, onChange }: any) {
  return (
    <FieldWrapper id={id} label={label} error={error}>
      <input
        id={id}
        name={id}
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        className={inputClass(!!error)}
      />
    </FieldWrapper>
  );
}

// --- SelectField Component ---
function SelectField({ id, label, value, error, options, onChange }: any) {
  return (
    <FieldWrapper id={id} label={label} error={error}>
      <select
        id={id}
        name={id}
        value={value}
        onChange={onChange}
        className={inputClass(!!error)}
      >
        <option value="" disabled>Select an option...</option>
        {options.map((opt: string) => (
          <option key={opt} value={opt}>{opt}</option>
        ))}
      </select>
    </FieldWrapper>
  );
}

// --- TextareaField Component ---
function TextareaField({ id, label, value, error, placeholder, onChange }: any) {
  return (
    <FieldWrapper id={id} label={label} error={error}>
      <textarea
        id={id}
        name={id}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        rows={3}
        className={`${inputClass(!!error)} resize-none`}
      />
    </FieldWrapper>
  );
}

// --- SuccessBanner Component ---
function SuccessBanner({ onDismiss }: { onDismiss: () => void }) {
  return (
    <div className="flex items-start gap-3 bg-emerald-50 border border-emerald-200 text-emerald-700 rounded-lg px-4 py-3 text-sm font-medium">
      <span className="text-xl leading-none">✅</span>
      <div className="flex-1">
        <p className="font-bold text-base">Message sent successfully!</p>
      </div>
      <button onClick={onDismiss} className="text-emerald-400 hover:text-emerald-600 transition-colors text-xl leading-none">×</button>
    </div>
  );
}

// --- Main App ---
const INITIAL_FORM: FormData = { name: '', phone: '', email: '', type: '', message: '' };

const INQUIRY_TYPES = [
  "Admission related",
  "Academics",
  "Placements",
  "Hostel / Accommodation",
  "General Inquiry"
];

export default function App() {
  const [formData, setFormData] = useState<FormData>(INITIAL_FORM);
  const [errors, setErrors] = useState<FormErrors>({});
  const [submitted, setSubmitted] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    if (errors[name as keyof FormErrors]) {
      setErrors(prev => ({ ...prev, [name]: undefined }));
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const validationErrors = validate(formData);
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    console.log('📬 Form Submitted:', formData);
    setSubmitted(true);
    setFormData(INITIAL_FORM);
    setErrors({});
  };

  return (
    <div className="h-screen w-full overflow-hidden bg-gradient-to-br from-slate-100 via-red-50 to-slate-200 flex flex-col font-sans">

      {/* ── Header ── */}
      <header className="w-full bg-white shadow-sm border-b border-slate-200 shrink-0">
        <div className="max-w-5xl mx-auto px-6 py-3 flex items-center justify-center">
          <img
            src="/logo.png"
            alt="VIT-AP University Logo"
            className="h-16 w-auto object-contain select-none"
            draggable={false}
          />
        </div>
      </header>

      {/* ── Main Content ── */}
      <main className="flex-1 min-h-0 flex flex-col items-center justify-center p-6">
        <div className="w-full max-w-[700px] h-full max-h-[850px] flex flex-col">

          {/* Card */}
          <div className="bg-white rounded-2xl shadow-xl shadow-slate-200/80 border border-slate-100 flex flex-col overflow-hidden h-full max-h-full">

            {/* Card Header */}
            <div className="px-8 py-6 border-b border-slate-100 text-center shrink-0">
              <h2 className="text-3xl font-extrabold text-slate-800 tracking-tight">Contact Us</h2>
              <p className="text-slate-500 text-base mt-2 font-medium">
                Fill out the form below and we'll connect with you.
              </p>
            </div>

            {/* Form */}
            <form onSubmit={handleSubmit} noValidate className="flex-1 overflow-y-auto px-8 py-6 flex flex-col gap-5 custom-scrollbar">

              {/* Success Banner */}
              {submitted && <SuccessBanner onDismiss={() => setSubmitted(false)} />}

              <InputField
                id="name"
                label="Full Name"
                value={formData.name}
                error={errors.name}
                placeholder="e.g. John Doe"
                onChange={handleChange}
              />

              <div className="grid grid-cols-2 gap-5 w-full">
                <InputField
                  id="phone"
                  label="Phone Number"
                  type="tel"
                  value={formData.phone}
                  error={errors.phone}
                  placeholder="e.g. 9876543210"
                  onChange={handleChange}
                />

                <InputField
                  id="email"
                  label="Email Address"
                  type="email"
                  value={formData.email}
                  error={errors.email}
                  placeholder="e.g. john.doe@vitap.ac.in"
                  onChange={handleChange}
                />
              </div>

              <SelectField
                id="type"
                label="Inquiry Type"
                value={formData.type}
                error={errors.type}
                options={INQUIRY_TYPES}
                onChange={handleChange}
              />

              <TextareaField
                id="message"
                label="Message"
                value={formData.message}
                error={errors.message}
                placeholder="Write your message here..."
                onChange={handleChange}
              />

              {/* Submit Button */}
              <div className="pt-2 mt-auto shrink-0 pb-2">
                <button
                  id="submit-btn"
                  type="submit"
                  className="w-full bg-vit-red hover:bg-[#6e1515] active:scale-[0.98] text-white font-bold py-3.5 rounded-lg text-lg tracking-wide
                    transition-all duration-200 shadow-md shadow-vit-red/20 focus:outline-none focus:ring-4 focus:ring-vit-red/30"
                >
                  Submit Message
                </button>
              </div>
            </form>

          </div>

          {/* Footer note */}
          <p className="text-center text-sm text-slate-500 mt-4 shrink-0 font-semibold tracking-wide">
            © {new Date().getFullYear()} VIT-AP University. All rights reserved.
          </p>
        </div>
      </main>

      {/* Hide default scrollbar but allow scrolling if absolute necessary on tiny mobile */}
      <style>{`
        .custom-scrollbar::-webkit-scrollbar { width: 4px; }
        .custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: #e2e8f0; border-radius: 4px; }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #cbd5e1; }
      `}</style>
    </div>
  );
}
