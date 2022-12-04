/** @jsxImportSource @emotion/react */
import React, { useState } from "react";
import { css } from "@emotion/react";
import { useEffect } from "react";
import { getCompanyInfo } from "../apis";
import { Loader } from "./Loader";
import { forwardRef } from "react";
import { Group, Text, Select } from "@mantine/core";
import _ from "lodash";

const SelectItem = forwardRef(
  ({ image, label, security, founded, added, ...others }, ref) => (
    <div ref={ref} {...others}>
      <Group noWrap>
        <div>
          <Text size="sm">{`${label} (${added})`}</Text>
          <Text size="xs" opacity={0.65}>
            {`Security: ${security} / ${founded}`}
          </Text>
        </div>
      </Group>
    </div>
  )
);

export const StockSelector = ({ onChange }) => {
  const [companyInfo, setCompanyInfo] = useState(null);

  useEffect(() => {
    const fetch = async () => {
      const companyInfo = await getCompanyInfo();
      const selectorValues = companyInfo.map((info) => ({
        ...info,
        value: info.symbol,
        label: info.symbol,
        group: info.sector,
      }));
      setCompanyInfo(selectorValues);
    };
    fetch();
  }, []);

  return (
    <div
      css={css`
        width: 500px;
      `}
    >
      {_.isEmpty(companyInfo) ? (
        <Loader />
      ) : (
        <Select
          label="Company Code"
          placeholder="please pick a company"
          itemComponent={SelectItem}
          data={companyInfo}
          onChange={onChange}
          searchable
          nothingFound="No options"
        />
      )}
    </div>
  );
};
