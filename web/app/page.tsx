export default function HomePage() {
  return (
    <section className="space-y-4">
      <h2 className="text-xl font-bold">Welcome to the Property Portal</h2>
      <p>
        This portal brings together a property value estimator and a market analysis dashboard.
        Use the navigation above to switch between the estimator and analysis applications.
      </p>
      <p>
        The estimator allows you to enter details about a home—such as square footage,
        number of bedrooms and year built—and receive a price prediction based on a
        regression model.  The analysis page visualises aggregate statistics of the
        housing dataset.
      </p>
    </section>
  )
}
