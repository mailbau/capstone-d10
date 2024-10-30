import React from 'react';

function InputField({ label, placeholder, type = 'text', name, value, onChange, readOnly }) {
    return (
        <div className="flex flex-wrap gap-4 items-end px-4 py-3 max-w-full text-base w-[480px]">
            <div className="flex flex-col flex-1 shrink w-full basis-0 min-w-[160px] max-md:max-w-full">
                <label htmlFor={name} className="pb-2 w-full font-medium text-stone-900 max-md:max-w-full">
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
                    className={`overflow-hidden self-stretch px-4 py-4 w-full bg-white rounded-xl border border-solid border-stone-300 min-h-[56px] text-stone-500 max-md:max-w-full ${readOnly ? 'bg-gray-100' : ''}`}
                />
            </div>
        </div>
    );
}

export default InputField;
