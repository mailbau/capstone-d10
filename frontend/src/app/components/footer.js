import React from 'react';

function Footer() {
    return (
        <footer className="flex justify-center items-start px-40 w-full text-base text-center min-h-[104px] text-stone-500 max-md:px-5 max-md:max-w-full">
            <div className="flex flex-col min-h-[104px] min-w-[240px] w-[960px]">
                <div className="flex flex-col justify-center px-5 py-10 w-full min-h-[104px]">
                    <div className="flex flex-col w-full min-h-[24px]">
                        <p className="w-full max-md:max-w-full">© 2023 Waste Management Solutions</p>
                    </div>
                </div>
            </div>
        </footer>
    );
}

export default Footer;