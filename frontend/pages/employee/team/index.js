import Layout from 'components/share/layout'

export default function Index() {
  return (
    <div>Danh sách nhóm làm việc</div>
  )
}

Index.getLayout = function getLayout(page) {
  return (
    <Layout>
      {page}
    </Layout>
  )
}