#ifndef FINDGUESTBYIDFORM_H
#define FINDGUESTBYIDFORM_H

#include <QWidget>

#include "baseform.h"

namespace Ui {
class FindGuestByIdForm;
}

class FindGuestByIdForm : public QWidget, public BaseForm
{
    Q_OBJECT

public:
    explicit FindGuestByIdForm(QWidget *parent = nullptr);
    ~FindGuestByIdForm();

    void clear() override;

private slots:
    void on_findGuestByIdBtn_clicked();

signals:
    void sendData(const QString &data);

private:
    Ui::FindGuestByIdForm *ui;
};

#endif // FINDGUESTBYIDFORM_H
