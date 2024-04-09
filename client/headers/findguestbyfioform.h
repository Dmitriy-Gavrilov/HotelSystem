#ifndef FINDGUESTBYFIOFORM_H
#define FINDGUESTBYFIOFORM_H

#include <QWidget>

#include "baseform.h"

namespace Ui {
class FindGuestByFioForm;
}

class FindGuestByFioForm : public QWidget, public BaseForm
{
    Q_OBJECT

public:
    explicit FindGuestByFioForm(QWidget *parent = nullptr);
    ~FindGuestByFioForm();

    void clear() override;

signals:
    void sendData(const QString &data);


private slots:
    void on_FindGuestByFioBtn_clicked();

private:
    Ui::FindGuestByFioForm *ui;
};

#endif // FINDGUESTBYFIOFORM_H
