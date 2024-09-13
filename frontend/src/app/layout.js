import "./globals.css";

export const metadata = {
  title: "Capstone D-10",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        {children}
      </body>
    </html>
  );
}
