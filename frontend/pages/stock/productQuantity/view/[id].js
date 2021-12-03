import axios from 'axios';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/router'
import { getDefaultLayOut, IconLink } from "utils/helper";
import Card from 'components/share/card';
import DataTable from 'components/share/datatable';

export default function ProductQuantityHistory() {
  const router = useRouter();
  const { id } = router.query;
  const baseUrl = '/stock/product-quantity';
  const backUrl = '../';
  const [location, setLocation] = useState({});
  const [product, setProduct] = useState({});

  useEffect(() => {
    if(id) {
      axios.get(`${baseUrl}/get-info/${id}`).then(result => {
        setLocation(result.data.location);
        setProduct(result.data.product);
      });
    }
  }, [id]);

  if(!location.id || !product.id) return <></>;

  return (
    <Card
    title={`Lịch sử tồn kho '${product.name}' tại '${location.name}'`}
      body={
        <>
          <DataTable 
            apiUrl={`${baseUrl}/history?location_id=${location.id}&product_id=${product.id}`}
          />
          <IconLink 
            href={backUrl}
            icon="arrow-left"
            variant="secondary"
            title="Quay lại"
            className="me-2"
          />    
        </>
      }
    />
  )
}

ProductQuantityHistory.getLayout = getDefaultLayOut;