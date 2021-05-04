/**
 * Cognito のカスタムメッセージトリガーに登録する関数です
 * API経由でアプリにリダイレクトします
 */
const cofirmEmailURL =
  "https://gcuoqt6cx9.execute-api.ap-northeast-1.amazonaws.com/confirm";
const userPoolId = "ap-northeast-1_HiRuznaNt";
const cognitoClientId = "7t7e3fkhvsfi97t7tpodnfr5hq";
const redirectURI = "https://cohabi.unison-8225.com/output";

const getEmailMessage = (userName, confirmationCode) => `Hi ${userName}
<br>
Click following link to complete signup.
<br>
<a href=${cofirmEmailURL}?client_id=${cognitoClientId}&user_name=${userName}&confirmation_code=${confirmationCode}&redirect_uri=${redirectURI}>Click Here</a>
<br>
Then, use username and password to signin.`;

exports.handler = (event, context, callback) => {
  //   console.log("EVENT", event);
  if (event.userPoolId === userPoolId) {
    if (event.triggerSource === "CustomMessage_SignUp") {
      event.response.emailSubject =
        "Welcome to Cohabi! Please verify your Email Adress.";
      event.response.emailMessage = getEmailMessage(
        event.userName,
        event.request.codeParameter
      );
    }
  }

  callback(null, event);
};
