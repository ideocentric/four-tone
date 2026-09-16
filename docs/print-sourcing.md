# Sourcing the printed parts

Where to have the head joints printed, and what they actually land at once tariffs
and shipping are added. The head joint is heavy for a printed part, so shipping
and import costs matter as much as the print price.

**Everything here was gathered on 2026-09-15.** Prices change, and the tariff rules
have changed repeatedly through 2026. Re-quote and re-check before ordering.

## What is being quoted

| Model | STL | Volume | Resin weight (at 1.1 to 1.2 g/cm³) |
| ----- | --- | ------ | ---------------------------------- |
| Head joint rev 02 (solid) | `mechanical/stl/head-joint_rev-02.stl` | 289.5 cm³ | 320 to 350 g |
| Head joint rev 03 (hollowed) | `mechanical/stl/head-joint_rev-03.stl` | 220.6 cm³ | 245 to 265 g |
| Fan caddy | `mechanical/stl/fan-caddy_rev-01.stl` | 8.3 cm³ | negligible |

Four voices need four head joints and four caddies. Quote **rev 03** for resin or
MJF: it is 24% less material for the same voicing geometry. For FDM either
revision works, because infill already hollows rev 02.

Upload the STL in **millimetres**.

## Quotes so far

| Source | Process | Price per head joint | Notes |
| ------ | ------- | -------------------- | ----- |
| JLC3DP (China) | SLA, 9600 resin | $26.35 print, **$41.19 landed** | Quoted for rev 02. Landed total covers build, the 40% tariff and shipping. |
| JLC3DP (China) | SLA, Imagine Black | $78.20 | Was cheaper in the past; the price rose substantially. |
| JawsTec (US) | SLA, basic resin | over $200 | Roughly eight times JLC3DP's 9600 price. |
| Xometry, Protolabs, Craftcloud | SLA | not yet quoted | All quote instantly from an uploaded STL. |

Craftcloud is a marketplace rather than a printer, so the shop's country decides
the import cost. Mexican shops looked viable when this was written.

## Import costs

The de minimis exemption, which used to let shipments under $800 in duty free, has
been suspended since 2025-08-29 and remains suspended. Every package now needs a
customs entry, so expect a carrier brokerage fee even when the duty is small.

| Origin | Duty on the part's value |
| ------ | ------------------------ |
| China (JLC3DP) | **40%** for resin prints, JLC's own published rate, prepaid at checkout on DDP shipping |
| Mexico, qualifying under USMCA and certified | about **0%** |
| Mexico, not qualifying or not claimed | about **15.3%**: 5.3% normal duty on plastic articles (HTS 3926.90.99) plus the 10% Section 301 tariff in force since 2026-07-24 |
| United States | none |

A part printed in Mexico from resin will probably qualify under USMCA, because
printing turns raw resin into a finished article, but the preference only applies
if the vendor certifies origin and the shipment claims it.

## Landed cost

```
landed = unit price x quantity + duty + shipping + brokerage
```

A JLC3DP order checked out at **$41.19 landed for one head joint**, which breaks
down as $26.35 for the print, $10.54 of tariff at 40%, and about $4.30 of
shipping. The tariff, not shipping, is the significant add-on: shipping is modest
even though the part is heavy.

| Route | Landed per head joint | Four head joints |
| ----- | --------------------- | ---------------- |
| JLC3DP, 9600 resin | **$41.19** (measured) | about $165 |
| US shop (JawsTec) | over $200 | over $800 |
| Mexican shop, USMCA certified | its quote + shipping and brokerage | needs to beat about $41 each |
| Mexican shop, not certified | its quote + 15.3% + shipping and brokerage | needs to beat about $36 each before duty |

**JLC3DP is the clear winner at present**, roughly five times cheaper per part
than the US quote obtained, even with the 40% tariff paid. A domestic or Mexican
shop only becomes interesting if it quotes near $41 per head joint delivered, or
if tariffs rise further. Shipping four parts at once spreads the shipping cost, so
the per-part landed price of a batch should be a little below $41.19.

## Questions to ask a vendor before ordering

1. **Does the price include duties (DDP), or are they billed on delivery (DAP)?**
2. **Mexico only: will they supply a USMCA certification of origin?** Without it,
   expect the 15.3% rate.
3. **Which resin, and what does it cost to ship the actual weight?** Four head
   joints are about 1 kg of parts plus packaging.

## Options that avoid shipping entirely

- **Your own FDM printer.** This is what the tested head joint was printed on. It
  uses the least material of any option, because infill hollows the block, and
  costs only filament. Print it in PETG or ASA for better durability than PLA.
- **A makerspace or library resin printer.** The part needs at least 150 mm of
  build height and fits in 67 x 67 mm on the plate. Usually charged by material.
- **Buying a large-format resin printer.** Four rev 03 head joints are only about
  1 kg of resin. If more pipes or revisions are likely, a printer can pay for
  itself against outsourced prices. Note that thick solid sections can warp on
  home resin printers, which the rev 03 cavity helps with.

## Sources

- [JLC3DP](https://jlc3dp.com/) and its [9600 resin data](https://jlc3dp.com/help/article/photosensitive-9600-resin)
- [JLCPCB U.S. Tariff Policy FAQ](https://jlcpcb.com/help/article/us-tariff-policy-faq), updated 2026-09-09
- [JawsTec SLA](https://www.jawstec.com/sla-3d-printing-service/),
  [Xometry SLA](https://www.xometry.com/capabilities/3d-printing-service/stereolithography-3d-printing/),
  [Protolabs SLA](https://www.protolabs.com/services/3d-printing/stereolithography/),
  [Craftcloud](https://craftcloud3d.com/)
- [Indefinite Suspension of the De Minimis Exemption (Federal Register)](https://www.federalregister.gov/documents/2026/06/24/2026-12670/indefinite-suspension-of-the-de-minimis-exemption-for-merchandise-arriving-through-all-modes-other)
- [HTS 3926.90.99 (USITC)](https://hts.usitc.gov/search?query=3926.90.99)
- [US-Mexico tariffs in 2026 (WhyLoyalty)](https://www.whyloyalty.com/blog/how-do-tariffs-impact-trade-between-us-and-mexico/),
  [USMCA exemption from Section 122 (FreightFigures)](https://www.freightfigures.com/articles/usmca-section-122-exemption-extended-2026),
  [Mexico retains preferential access under USMCA (Holland & Knight)](https://www.hklaw.com/en/insights/publications/2026/07/mexico-mantiene-acceso-preferencial-bajo-el-tmec)

The tariff sources are trade advisories and news, not official rulings. For a firm
answer, check the classification at [hts.usitc.gov](https://hts.usitc.gov) or ask
the carrier's brokerage desk.
