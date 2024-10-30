import React from 'react';

function InputField({ label, placeholder, type = 'text', name, value, onChange, readOnly }) {
    return (
        <div className="flex flex-col items-center w-full px-4 py-3 max-w-lg">
            <label htmlFor={name} className="pb-1 text-sm font-semibold text-gray-700 text-center">
                {label}
            </label>
            <input
                type={type}
                id={name}
                name={name}
                placeholder={placeholder}
                value={value}
                onChange={onChange}
                readOnly={readOnly}
                className={`px-4 py-3 mt-1 w-full bg-gray-50 border rounded-md border-gray-300 text-gray-700 transition-shadow duration-200 focus:outline-none focus:ring-2 focus:ring-blue-300 ${readOnly ? 'bg-gray-100' : 'bg-white'
                    }`}
            />
        </div>
    );
}

export default InputField;
