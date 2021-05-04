/**
 * 指定されたredirect_uriにリダイレクトします
 * API Gatewayで、/confirm GETに登録します
 */
const https = require("https");

const cognitoAuthUri =
  "https://cohabi-user-alias.auth.ap-northeast-1.amazoncognito.com/confirmUser";
const getSuccessResponseBody = (redirectUri) => `
    <HTML>
    <HEAD>
        <META HTTP-EQUIV="Refresh" CONTENT="0; URL=${redirectUri}">
        <TITLE>Success</TITLE>
    </HEAD>
    <BODY>
        <H1>Success Email Confirmation</H1>
        <A HREF="${redirectUri}">here</A>.
    </BODY>
    </HTML>
`;

exports.handler = (event, context, callback) => {
  const err = null;

  const {
    client_id: clientId,
    user_name: userName,
    confirmation_code: confirmationCode,
    redirect_uri: redirectUri,
  } = event.queryStringParameters;

  if (!clientId) err = "client_id param is required";
  if (!userName) err = "user_name param is required";
  if (!confirmationCode) err = "confirmation_code param is required";
  if (!redirectUri) err = "redirect_uri param is required";

  if (err) {
    callback(null, {
      statusCode: "400",
      body: JSON.stringify({ error: err }),
      headers: {
        "Content-Type": "application/json",
      },
    });
    return;
  }

  https
    .get(
      `${cognitoAuthUri}?client_id=${clientId}&user_name=${userName}&confirmation_code=${confirmationCode}`,
      (res) => {
        callback(null, {
          statusCode: "301",
          body: getSuccessResponseBody(redirectUri),
          headers: {
            "Content-Type": "text/html; charset=UTF-8",
          },
        });
        return;
      }
    )
    .on("error", (e) => {
      console.error(e);
      callback(null, {
        statusCode: "400",
        body: JSON.stringify({ error: e.message }),
        headers: {
          "Content-Type": "application/json",
        },
      });
      return;
    });
};
