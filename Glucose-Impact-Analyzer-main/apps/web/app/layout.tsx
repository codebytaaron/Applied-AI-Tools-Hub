export const metadata = {
  title: "Glucose Impact AI",
  description: "Estimate glucose impact of meals"
};

export default function RootLayout({
  children
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body style={{ margin: 0, fontFamily: "Inter, system-ui" }}>
        {children}
      </body>
    </html>
  );
}
