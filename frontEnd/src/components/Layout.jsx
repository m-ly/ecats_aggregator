import Form from "./Form";
import Header from "./Header";

function Layout() {
  return (
    <main className="flex flex-col relative mx-auto items-center">
      <Header />
      <Form />
    </main>
  );
}

export default Layout;
