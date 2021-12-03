import Layout from '../components/share/layout'

export default function Index() {
  return (
    <>
    </>
  )
}

Index.getLayout = function getLayout(page) {
  return (
    <Layout>
      {page}
    </Layout>
  )
}