import {Col, Row} from "antd";
import {ConceptCard} from "../common/card";

interface BatchSelectProps {
    label: string,
    model: string,
    dataset: string,
}

export function BatchSelect(props: BatchSelectProps) {
    const {model, dataSet, label} = props
    const conceptsFromImage = [
        {
            src: "https://cdn.shopify.com/s/files/1/2660/5202/products/pas2gqbd_ac_1400x.jpg?v=1607548205",
        },
        {
            src: "https://images.ctfassets.net/q5lwz1whkyct/2CQG2VjnaFisjskxGEL4dn/f3756e2c64721008e3b4d28d505b0477/Haven-Heathered-Gray-01_2x__2_.jpeg",
        },
        {
            src: "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAoHCBYVFRgVFRUYGBgYGBgcGBgYGhkcGRgYGBgZGRgcGRodIy4lHB4rIRgaJjgmKy8xNTU1GiQ7QDs0Py40NTEBDAwMEA8QGhISHjQkJSs1NDQ0NDE0NDQxNDQ0NTQ0NDQ0NDQ0NTE0NDQ0NDQ0NDE0MTQ0MTQ0NDQ0NDQ0NDQ0NP/AABEIAMYA/gMBIgACEQEDEQH/xAAbAAABBQEBAAAAAAAAAAAAAAACAAEDBAUGB//EAEIQAAIBAgMDBwkGBQQDAQEAAAECAAMRBBIhMVFhBQZBcYGRoRMiMlKSscHR8BRCU2JyshUWI6LhB4LC8UOT0vIk/8QAGAEBAQEBAQAAAAAAAAAAAAAAAAECAwT/xAAgEQEBAQEAAwACAwEAAAAAAAAAARECEiExE0EDYaFR/9oADAMBAAIRAxEAPwDuMV6PYPeIkMbE+j2H4RkMCZTDEjWGIEgMcQBCEArx4EeAcUaJVvAeMJKtOHlgQZYsssRQK1oxlm0ErArxQnWNlgDFCIgwFGijQFGjxoDRRQTAUa8URkDXiMUYwFBjmNAWI9A9R9xgUzoIdX0T9dBkNE6CUWlhCRrDEAxCgCEIBRRo8BxJqUgk1KBNFGvFKh4o0UBRjFEYVE8JYDQ0kCKwGSSRoEJWCRJzAZYEUaGywCIAmNHMYwGjRzGkUxiijQGjRzGgO3omV8MfNEn6DKuFPmiVFxTDEiUyQGAYhCADCBgFHg3ivAd3AFyQANpOgkdLlCn+Intr85i88Xthn/Un71nn3lZZEewfxKl+Kntr84v4lS/FT21+c8e8uY/lzLg9f/iVL8VPbX5xfxOj+LT9tfnPIDXME4gxg9g/idH8Wn7afOCeVKP41P8A9ifOePtiDIjiDeMHsLcp0fxU9tfnCTlKl+Kntr8548MQYxxBjB7L/EaX4qe2vzjfxGl+LT9tfnPGvtBjfaDGD2b+IU/xE9tfnF9vp/iJ7a/OeMmuYPlzGD2c4yn66e0vzjHFJ66e0PnPFzXMB60Yr2xXBFwQRw1jGcJ/p9XOSoL6Z7/2r8p3SG4mQ5gmORBMilGivGJgKNFeMTAcdPbKeDPmiWxtI4mUsIdLcTNVF1TJQZApkoMgkEcQAY4MCSMY14xMDD552OFcHpKDqOddZ5q9Ij7x8J6VzxF8K/Wnb566Tzd2b1T4TUAqg9c+ELyP5j4Q8BhTUqohOQO6rnIvlzGwNri+vGb+K5k4pD5mSou8NkbqKtoO8xbIslrnTR/OfCN5H858Jer8jYtPSwtX/aA/ihMoVldPTpuv6lK++NhlM1EeufCRGlr6Z7ozVjuMDyp9UwiYUfznujGj+c90AVD6piLt6jd0AvJfn8I3kvz+EBnPqmWsLgq9T0KFRwekI2X2tg74WRAaX5vCCaf5/CdBhuaOKf0kSmNPTcE23gJm7jaS8tcgUsNTZmd3fKbZQFUN0XGpI7b7OzN6jU46rmDT/P4QWpfm8IAqE/dbuMRc+qe4zTDt+YVsj29fXuE76h6InAcwktTc73+FvhO7oOANZhU5EjYQ8449x+UYsOPcY2f9MqIwYTOOPcflABB1EksphRoopQ76OeuUMMdW/U3vl/E6P1gfL4TMot57/qPvmqjRQyQGV1aSBpBLeRPjEBsXW+7MJT5WxJSk7KbGwAO7MQPjKPJeKRMNUcDztNoOzMqD9xgbtPEq3osD1EGS5pwa8olMTTy6CohzAbMygWPgfCdnSqXAMDJ55H/+Z+DJ+9RPPmq8Z6Dzte2GfiUB6i6AzJw3MB3RHFSl56hgBnOjC41sOg7pYORNa2oOo2dmye3YaoHVXXYyhh1MLj3zhz/pq/4yey/z1nbcl8nNSo06ZYEoiJcA2OVQt/CZ6mt89SfUh0iD36ZI1De3hIHKjpMxldJ1KlsNwlbEIm0op61BgvigDbxPjK1TF3Oh0IFui9/+7dcauKtXBUsQHWolxmA0upNrMLMtjbYNvQeMalzdwqiwoIf1Xf8AeTJ6mLINrjS9+IHuEn+1UlTyjuVXYTt14aRNvwtk+wFLB009Cmi/pRR7hJWeY1XlR3F0Aprc2L+ezDoITTL2mUmxb3U+WbQ7CosddjAWuO2PGn5OW/Uec1znw+ei6jblJX9S6gdtrdsu4bljKwWsgZS1vKoxUKCNM6dGt9b21HTt6BKVF1DKqsDqCfOB74nFL/LzmPEeTcJWrKWpU3dVBLMqkqLbbtsvwveQGtptnq3PPFeSwtQ5iLrkVV0Az+boBs2k9k8fRV3eJnV53oHMM/03P553GAe7L2/GcNzJf+gf1H3mdrya3nL1fGYqix3Kjo7KFUgWte9zcA7+MrryxUtcog9r5ylzixYR2JF/OTT/AGqTaQ1MQoTNe4tpr6V/fMXXSTn/AB0mAxRqIxYAEEjS+4Hp65nYF7i3E+BIlnkZro36v+ImbgH2/rcf3tLzWepluNIwbxExrzbKTHekDw+vfMhWtUccfeAZrcoHRTx+H+Jh1HtVPEA+FvhNVI01aZ3LeKdAuQNbpyi9zcaHdp9aS4jwMXisiMw1YDQcdgmbNjXNy6oYDlMMn9ZLixNyt0uMpF+wnW33b9WU9ZS2JFMgoKKXC6KH8qhYLwsN+28qvjq3nKXN2vqwBIuLXHROX5KxVemjKqsUYWBBUXGgG0jS4E58y7a31ZfkblSqDiaGuoFS43aHSd9g381eqeR4XEP9qR6ilS+cDN6tibg77jxnqOCrrlXUbJ1c6DnSw+zVL/kt151y+Npq8xMYamGQMbmmWQ9S2Kf2so7Jh86GzYapbWwVuxXVj4Axv9LsZmNanuyOO0FH9ySo9HgkxyZXerKhsQ+kzar3231PRfvluq+nCVKiA2J2Tn1HbixnYnQ3uToQNttu3rlV6gA6ATfU9HVffb66NCu4UM2g3niTvG3baUCxZrAFtdLAm23p4aTk7RWquRaxIHSQdbgnS2022aTLo1Q9Wx9CmM2Um4LE2QEdhbX1Zu1KL9KN7B+UjyONiP2KflLzc/Sdc+X7ZdaoSek95jU8O7fdNt50980AlU/cfsViPdJ/4dXbYhHWyj4zXnb8jH4+Z9rGdchsSLm/+QZa5D5S8nUFBmApsP6YtqGvdl47b3O8cZPi+beIcqVKAre4ZjqD1Ai+kzcTyFikem3kjdG2rkfTTZY3Gyb5tz25dSb6afPjDeUwVYXsVXOP9jB/EKR2zx1Q3DvnvBRmTK6NYixDKbEEWI2Txjl3kw4dyupTMQrcR908bajeDffa6knp1nNB7URxZveZ2PI1a75dw+Inn/NmrlpqOs95vOlwXLFOi+d2sLbBqx1B0AkvxY1OcOFFR2BYixU6C/3Ft9cZFhsOqIEJvt27r3+MGhypTxNZ8mfLkBLaLZvNGXYb6XMufZ6ZNldiRtXQlh0brbpiyt83me/2v8kCyOOgHTqyiY+AfV/1v+4zWwbohZAxJIDAEa2INtenYdZzeCxNncfnc97GWSxm2XcdCGj3kKPpDzTTKxj/AEL7iD8PjOdxLf1Ad6+4n5zosTqjfpPgJy2Mfz0P6h7pqkW8bi8ig79L7tnzmTUxCsCNbnpsx137JY5VN0HWPeJlKDOXXVldOeZYE4QksWqsSwtohFtOjjrAw3ICZQufQWt5j9HbLKFtw8ZoUqbLbMLXUML9KtsI4aGY2tZGOeREDq5Oq3t5j9PbNWiVFlCknYBlYXO4abZpYDAPWcItt5JvZR0k987LA8mUcMua122F29Ik6WHqjgPGb5lrNsnpwuA5r4vE0nFQCgtS1s4uwHmnSmDcbLWYgzpuavNdMCrMz53bQvlygLoQqrc6aXOuptuE26mJJ2Bh2W8TaVGcNtNzuvfwE15YxObVipixuJtwMgauT6KdpsPedJE5Qfcf/bTf/wCZXr1r/cqADo8mbHrBFzHlWpxF9MUdhFv9yn3G8L7Yj6eabGx6bHiOiYroh/8AEyneEynutBOEQvntWGgAABAsL7dLnb0noEz51r8cdBSqITYEXtsG2TEzFuMpGVzf1gx7r3tBpuUHpMf1Fj4ZbeE15Rm/x1tHukT4iw4zPWozbWa3D/qA6H7qX4sXHjlMecPx1Yeqx/7kf2oDTZaUfso2sq9S1H97ER3TNYByoBv5rrfqJuxI7pPNfx/21sK/3j1W6b8ZM73mYj5VNiNTrbMT16fKC2NfYFY9qD91pfKJ+OtFWMq4/A06yFK1NXU9DqDr0EdKniNRImqM33mHUyDusP8AMSViLKrLp0Frm3dL5RPCuO5X5lvSXNgyWAN/JufOtrornRuprHiTORxuFZG/qZqbG5yOljt1sSRcceM9oWqekA9V5U5QwtKupp1EBB6DtHEHoPHbJffypNn2PI+T8U9LNkrWzWvbINl94bTUWt8ZbHK1b8a+uvodv3OuTc4OQnwr6gvTJ8x/+L7m8D0dIGQtThMXqusk/Tok5wsAGspqhcmfyhAPmMucrksHBI0Ay2GyUeTcWVuatQMxI1W3QAOG6UFf8sLOPVmfKnjHWYHllGYIpJJ6txPQeE2ExF5w3JTf1AbW0+DTpqVSb5rHUyunvdSOBnG4x/QO5rd4M6+mejjONxwOoG0MLdhnSsRLyg/9MdYmerjevePnL2PRhSuQRr/xaUlzGce/rrx8Sow9ZfaHzlnDFRc3XsI+croG+jLuGRrf5kbdrzXpKtAPbVySW3gEgdmh75qmiXN2JC9AG3tPR2aypyEhNFGYZbKABvtoG6jt7ZpM87Seo4W+6gGES98gJ/Ndv3XtJr22QC8E1Jpm20ZMEwDUi8pAO8V4GeMXkBxQM8WeAcV4GeLPAK8Ei/RGzwfKSgxTX1R3CPsgZ4s8gctGIvBLxvKQAfDodqjut4iUP4LTBJTOpOvpuy3/AEuSB2Wmj5SLygjIs6sYGMoEKadVQ9NxlJF7Dr6U4a6Hpvaeccv8kthnC5iyNqj7wNoNvvC467g8B7DWsRY7DtnG85sBnoOlsxQh00udOgcbEjtmeufTXPXt58j8TJBU4mVhlO7uEIAcO4Tk7NPkypd+z5zoaLzmeSrZzbd8p0FEzUY6+uvRtT1znOU8E5qPltY+cL7zrbvvOkqU8jZiwAY7GNrk7j8IPKa0XQoza/dKgtlYdOmlp1rlHH4vHl6ZQqB03BvsBHxlOlWvsH1vmnU5KzqU1FwR5u3rvaVU5lg/+St7Sj3rOF9/XaevgFqaaTouavJ5rvme+RLZr7DtIUdZueq+8TMwXMEO2Xy9VR0kMpsOHm7Z6TyfgqeHprTprlRBYakknpZmOrMd5m+ed9s9dZ6WneQ5oDvALTq5CZ4BMV4N4BXiBjRQHLQLwXMaBJeK8COIBgxRCJmgCTGvBZ42aBJmiEEGEIAuZEzQqjSHNAPNCBgAQhAIiUOUsOzIwQgPlOQnYGtpfhe0v3jVV0geG16TI7I4KupIYG1wemMpE7vnnzeOIHlKRCVU26Ah0HQfzDoO643W4heQcR+Ins/4nHrnHbnrV/kKrldjs80jTrSdPRxy+sfGc/yRyM6AlnViTtAI0sNLdk3KeC4zO4ua7DF4pGXLkzbidLHeDt8JnpR6T3b5N5M7ojSY7T9dk111rMmHV8o2CMcUNwjHC7zJEwqjUzLTU5C1DtxA7h/mXsQ9pX5NslO+zMSfh8JFiawvqZ25+OPXujNSErSl5TXXZJ1qSokd4OeZuO5Tp0z/AFKiJwd1UnsJuZQfnZg121wf0o7eKqRA6EGItOfPO3BgZvLjsVyfZy3kA57YO/pv/wCt/wD5lHTNHUzlTz4wnrP/AOto689sIfvuOtH+F4HVFo6mc9h+d2Df/wA4W3rK6/uWXcPy/hm2YiieHlEB7rwNYtIi057lDnjhqZCmqrEm3mXe3XkvaQNzyw20VP7XuB1ZZB0hMWacbU5/UA2UJUI9YBR3AsDJ6HPTCn0ndOtHP7QYHW02hl5z6c7cERYYga71ce9ZYHOTCHQYml7ajwvAv1XjJKq4xH1Rgw6CNh6pYpsN8KsXjZ7anqHXIDV6AYDuCRr0wi2hubcJINRK3lVB0PAw1cDplFbE07G85jlHDBH0HmtqOB6R9b51eIqoRbMMx2Dp7phcpWKG/RYj3THU2N83KzqMsgSrSMso84uzpSN8BnG8Su5jU0v9fWk05rNKxO+SsoO33waaw8s1IzaPF1siqBtsOocTPNufGIe+GdHdc4qucrFfwsl7Hd753fKTnIVvYsuUHr0+M43/AFBpALQI2KXUdoS37Ztlicn858TRXKrhx0eUBcjtuD33lfEc5MXWBD4h7XPmpZBbd5gBI6yZnQaPT+r5TSCCdO/bxhARR4DWiIjxXgDaPaIRXgIiCRCMa8CGoNV/V8DJSJHU9Jev4GSGArRRXjGAxEYiEYxgCBu06vjHR2X0WYdRI90RMG8CYY6qNlaqBuFR7d15ZTl7ErqMQ/aQ37gZnmCTA3sJzwxKqQxRzc+c6nNt6cpA8Jn8qc4sVVuXruo6Fpkoo4eabntJmfSPm9p95g1BfTfIr1bm3VLBtl1y3JGpBB2npOm2T8pfeG//ABMHm/j8lQA+i9lPC50P1vM1+UKwZ7LqBpffM76a/aqi2k4kKjo+uuWVScrHSXW0qXMsIkYDokqiajFolFo7GNGtNMoKrTOxShlIKg7rgGx2aTXaneRVaF4Hlp5CrDag7Cplf+XKrOWbzRYWAJ279J6mcLwgthBu+uiSTGrdeYNzdfj7RiXm456T7RnpTYMbohhBbYJdqPNTzcqbz7RjrzbqcfaM9GGFG6SLhPoDhG0eanm1U3n2jH/lqp9MZ6T9kG6N9l4RtHm7c2am/wDuMD+XKnH2jPSxhBw6dv19axHCjhG0eZvzaqePrH66Yhzaqb/7jPSnwo8fr6+glwo3DwjaPN35s1N59oxhzYqH/wDU9L+yj64RxhhG0eaHmxVte/8Adukf8tVePtT1AYYQRhRG0eZ/y1V3nvMD+Wqo3989P+zDhGOFHyjajzD+W6nHvkTc36vHvnqa4UdkFsEt9n/e/wBwjaryheRq408mTbpuuvjLOC5Gq5vPSw01Yg91jPTPsi32e+J8IN31eT2u+nJ4XBlSDul4ZiTpN1cMBH+zQms2jSli1uH0ZdWhwh+S+tIw1eWSXjxQHivFFKggIoooDRMN0UUCFl+tPlHce742+UUUAcokiILfW+KKAJAiA+rRooDEfX11RARRQGI+HvtEB9W6uMaKAeXTt/xHWn9axRQF5K+6Co1+t8eKAwSC6+8DviigPkPCCy/KKKBE1vq0Skce4cYooDlBe0ICKKFR2hRRQP/Z",
        },
        {
            src: "https://content.valuecityfurniture.com/images/product/charleston_gray_king-bed_1855484_530554.jpg?akimg=product-img-433x433",
        },
    ]

    function handleConceptIsRelevant(name: string, decision: boolean) {
    }

    return (
        <>
            <h3>Correct images</h3>
            <p>Select images that match label: <b>{label}</b></p>
            <br/>
            <Row>
                {
                    conceptsFromImage.map((el, i) => (
                        <Col key={i} span={8} style={{marginRight: 50, marginBottom: 20}}>
                            <ConceptCard

                                imageUrl={el.src}
                                imageWidth={200}
                                onSelected={handleConceptIsRelevant}
                            />
                        </Col>
                    ))
                }
            </Row>
        </>
    )
}